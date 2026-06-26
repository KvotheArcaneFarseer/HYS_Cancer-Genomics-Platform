import requests
import pandas as pd

BASE_URL = "https://www.cbioportal.org/api"
HEADERS = {"Accept": "application/json"}

CANCER_STUDY_MAP = {
    "breast": "brca_tcga_pan_can_atlas_2018",
    "lung":   "luad_tcga_pan_can_atlas_2018",
}

MUTATION_PROFILE_MAP = {
    "brca_tcga_pan_can_atlas_2018": "brca_tcga_pan_can_atlas_2018_mutations",
    "luad_tcga_pan_can_atlas_2018": "luad_tcga_pan_can_atlas_2018_mutations",
}


def get_study_id(cancer_type: str) -> str | None:
    return CANCER_STUDY_MAP.get(cancer_type.lower())


def get_entrez_id(gene_symbol: str) -> int:
    url = f"{BASE_URL}/genes/{gene_symbol.upper()}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["entrezGeneId"]


def get_sample_count(study_id: str) -> int:
    url = f"{BASE_URL}/sample-lists/{study_id}_all/sample-ids"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return len(response.json())


def get_mutations(study_id: str, gene_symbol: str) -> list:
    molecular_profile_id = MUTATION_PROFILE_MAP.get(study_id)
    if not molecular_profile_id:
        return []

    entrez_id = get_entrez_id(gene_symbol)

    url = f"{BASE_URL}/molecular-profiles/{molecular_profile_id}/mutations"
    params = {
        "sampleListId": f"{study_id}_all",
        "entrezGeneId": entrez_id,
        "projection":   "SUMMARY",
    }

    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def get_mutation_frequency(mutations: list, total_samples: int) -> dict:
    mutated_samples = len(set(m["sampleId"] for m in mutations))
    percentage = round((mutated_samples / total_samples) * 100, 1) if total_samples else 0
    return {
        "mutated_samples": mutated_samples,
        "total_samples":   total_samples,
        "percentage":      percentage,
    }


def get_common_mutations(mutations: list, top_n: int = 4) -> list:
    if not mutations:
        return []

    df = pd.DataFrame(mutations)
    if "proteinChange" not in df.columns:
        return []

    counts = (
        df.groupby(["proteinChange", "mutationType"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(top_n)
    )

    return [
        {
            "amino_acid_change": row["proteinChange"],
            "count":             int(row["count"]),
            "type":              row["mutationType"],
        }
        for _, row in counts.iterrows()
    ]


def fetch_cancer_profile(cancer_type: str, gene: str) -> dict | None:
    study_id = get_study_id(cancer_type)
    if not study_id:
        return None

    total_samples = get_sample_count(study_id)
    mutations     = get_mutations(study_id, gene)

    return {
        "cancer_type":        cancer_type.title(),
        "gene":               gene.upper(),
        "study_id":           study_id,
        "mutation_frequency": get_mutation_frequency(mutations, total_samples),
        "common_mutations":   get_common_mutations(mutations),
        "biological_function": {
            "summary":           "",
            "affected_pathways": [],
        },
        "targeted_therapies": [],
        "literature":         [],
        "disclaimer":         "This tool is for research purposes only. Not for clinical use.",
    }