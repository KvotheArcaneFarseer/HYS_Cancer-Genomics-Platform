# Data Sources

## Purpose

This document defines which public data sources the Cancer Genomics Platform should use, what each source contributes, and when each source should be integrated.

The platform should favor structured, traceable, public evidence. Generative AI should not be treated as a primary data source.

---

## Current Source

## 1. cBioPortal

### Role

Primary cancer genomics source for the MVP.

### Current Usage

The backend currently uses cBioPortal to retrieve:

- Study-specific sample counts
- Gene Entrez IDs
- Mutation records
- Mutation frequency
- Common amino acid changes

### Current Supported Studies

| App Cancer Key | Cancer Type | cBioPortal Study ID |
|---|---|---|
| `breast` | Breast cancer | `brca_tcga_pan_can_atlas_2018` |
| `lung` | Lung adenocarcinoma | `luad_tcga_pan_can_atlas_2018` |

### Strengths

- Provides convenient API access.
- Aggregates large cancer genomics datasets.
- Good for mutation frequency and study-level genomic exploration.

### Limitations

- Does not by itself explain biological meaning in beginner-friendly language.
- Does not replace curated pathway databases.
- Study IDs and molecular profile IDs need careful mapping.
- External API failures must be handled gracefully.

---

## Near-Term Sources

## 2. Static Curated Gene Knowledge

### Role

Immediate next source for the Gene Knowledge Engine.

### Format

A local JSON file should be used first.

Example path:

```text
backend/data/static_gene_knowledge.json
```

### Data Fields

```json
{
  "TP53": {
    "gene_name": "Tumor protein p53",
    "summary": "Tumor suppressor involved in DNA damage response, cell cycle arrest, and apoptosis.",
    "pathways": ["DNA damage response", "Cell cycle checkpoint", "Apoptosis"],
    "cancer_relevance": "Frequently mutated across many cancers and often associated with genomic instability.",
    "sources": []
  }
}
```

### Why This Comes Before AI

This gives the platform reliable explanations immediately while avoiding hallucinated biomedical summaries.

---

## 3. PubMed / NCBI E-utilities

### Role

Literature retrieval.

### Intended Usage

Given a cancer type and gene, retrieve:

- Paper title
- Authors
- Year
- Journal
- Abstract snippet
- PubMed link

Example query:

```text
TP53 breast cancer
```

### Initial Scope

For MVP expansion, return metadata and abstract snippets only. Do not summarize with AI yet.

### Later Scope

Once retrieval is reliable, add citation-aware AI summaries using only retrieved abstracts.

---

## 4. Reactome

### Role

Pathway evidence.

### Intended Usage

Retrieve or map genes to biological pathways.

Examples:

- `TP53` → DNA damage response, apoptosis, cell cycle checkpoints
- `PIK3CA` → PI3K/AKT signaling
- `BRCA1` → homologous recombination repair

### Why Useful

Pathway analysis makes the project more biologically meaningful than mutation frequency alone.

---

## 5. NCBI Gene

### Role

Gene metadata.

### Intended Usage

Retrieve:

- Official gene symbol
- Full gene name
- Aliases
- Summary description
- Organism information

Useful for validating gene symbols and reducing bad user input.

---

## Later Sources

## 6. CIViC

### Role

Curated cancer variant interpretation.

### Intended Usage

Use for clinical/evidence-level variant interpretation later.

### Caution

CIViC brings the project closer to clinical decision-support territory. Any integration must preserve the research-only framing.

---

## 7. COSMIC

### Role

Somatic mutation catalog.

### Intended Usage

Potential future source for mutation prevalence and cancer mutation patterns.

### Caution

Check access/licensing constraints before integration.

---

## 8. DepMap

### Role

Cancer dependency and functional genomics.

### Intended Usage

Future feature for connecting genes to cancer cell-line dependency patterns.

---

## 9. GDSC / Drug Sensitivity Sources

### Role

Drug sensitivity evidence.

### Intended Usage

Potential future drug-response analysis.

### Caution

This can easily be misread as treatment recommendation. Use evidence-ranking language, not prescription/recommendation language.

---

## 10. ClinicalTrials.gov

### Role

Clinical trial matching.

### Intended Usage

Eventually match cancer type and gene/mutation terms to relevant clinical trials.

### Caution

This is out of scope for the first demo. It is a later expansion after the knowledge and literature layers are stable.

---

## Source Integration Priority

### Phase 1

- cBioPortal
- Static curated gene knowledge

### Phase 2

- PubMed
- Reactome or curated pathway table
- NCBI Gene

### Phase 3

- CIViC
- ClinicalTrials.gov
- Drug evidence sources

### Phase 4

- DepMap
- GDSC
- Multi-omics datasets

---

## Data Governance Rules

1. Use public datasets only for the MVP.
2. Do not ingest patient-identifiable data.
3. Clearly label all outputs as research/educational content.
4. Store source names and source URLs with every generated claim when possible.
5. Prefer structured data over AI-generated text.
6. Add generative AI only after source retrieval is stable.
7. Cache external data where reasonable to reduce API latency and failure risk.

---

## Immediate Next Data Task

Create a small curated gene knowledge file for the first demo genes:

- `TP53`
- `PIK3CA`
- `BRCA1`
- `BRCA2`
- `EGFR`
- `ALK`

This should power biological function and pathway sections before PubMed/RAG are added.
