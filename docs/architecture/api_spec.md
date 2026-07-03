# API Specification

## Overview

The backend API should expose research-oriented endpoints for querying cancer genomics evidence. The API should not provide diagnosis, clinical recommendations, or medical advice.

Current backend framework: **FastAPI**  
Current frontend: **Streamlit**  
Current local backend URL: `http://localhost:8000`

---

## Current Implemented Endpoints

### `GET /health`

Purpose: Confirm that the backend is running.

#### Response

```json
{
  "status": "ok"
}
```

---

### `GET /data`

Purpose: Return cancer/gene mutation information from cBioPortal.

#### Query Parameters

| Parameter | Type | Required | Example | Description |
|---|---:|---:|---|---|
| `cancer_type` | string | yes | `Breast` | Cancer type selected by user. Currently mapped internally to cBioPortal study IDs. |
| `gene` | string | yes | `TP53` | Gene symbol. |

#### Example Request

```text
GET /data?cancer_type=Breast&gene=TP53
```

#### Current Response Shape

```json
{
  "cancer_type": "Breast",
  "gene": "TP53",
  "study_id": "brca_tcga_pan_can_atlas_2018",
  "mutation_frequency": {
    "mutated_samples": 0,
    "total_samples": 0,
    "percentage": 0.0
  },
  "common_mutations": [
    {
      "amino_acid_change": "R175H",
      "count": 10,
      "type": "Missense_Mutation"
    }
  ],
  "biological_function": {
    "summary": "",
    "affected_pathways": []
  },
  "targeted_therapies": [],
  "literature": [],
  "disclaimer": "This tool is for research purposes only. Not for clinical use."
}
```

---

## Recommended API Evolution

The current `/data` endpoint works for the prototype, but the name is too vague. As the system grows, replace or supplement it with more explicit endpoints.

---

## Proposed Endpoints

### `GET /api/v1/gene-profile`

Purpose: Return the full canonical profile for a gene within a cancer context.

#### Query Parameters

| Parameter | Type | Required | Example |
|---|---:|---:|---|
| `cancer_type` | string | yes | `breast` |
| `gene` | string | yes | `TP53` |

#### Response

```json
{
  "gene_symbol": "TP53",
  "cancer_type": "breast",
  "study_id": "brca_tcga_pan_can_atlas_2018",
  "mutation_frequency": {
    "mutated_samples": 350,
    "total_samples": 1000,
    "percentage": 35.0
  },
  "common_mutations": [],
  "biological_function": {
    "summary": "TP53 is a tumor suppressor involved in DNA damage response, cell cycle arrest, and apoptosis.",
    "source": "curated_static_knowledge"
  },
  "affected_pathways": [
    {
      "name": "DNA damage response",
      "source": "curated_static_knowledge",
      "source_url": null
    }
  ],
  "literature": [],
  "targeted_therapies": [],
  "evidence_sources": [
    {
      "name": "cBioPortal",
      "url": "https://www.cbioportal.org/"
    }
  ],
  "disclaimer": "For research and educational use only. Not for clinical use."
}
```

---

### `GET /api/v1/supported-cancers`

Purpose: Return the cancer types currently supported by the application.

#### Response

```json
{
  "supported_cancers": [
    {
      "display_name": "Breast Cancer",
      "query_key": "breast",
      "study_id": "brca_tcga_pan_can_atlas_2018",
      "source": "cBioPortal"
    },
    {
      "display_name": "Lung Adenocarcinoma",
      "query_key": "lung",
      "study_id": "luad_tcga_pan_can_atlas_2018",
      "source": "cBioPortal"
    }
  ]
}
```

---

### `GET /api/v1/literature`

Purpose: Search literature for a cancer/gene pair.

#### Query Parameters

| Parameter | Type | Required | Example |
|---|---:|---:|---|
| `cancer_type` | string | yes | `breast cancer` |
| `gene` | string | yes | `TP53` |
| `limit` | integer | no | `5` |

#### Response

```json
{
  "query": "TP53 breast cancer",
  "results": [
    {
      "title": "Example paper title",
      "authors": ["Author A", "Author B"],
      "year": 2024,
      "journal": "Example Journal",
      "abstract_snippet": "Short excerpt from abstract...",
      "url": "https://pubmed.ncbi.nlm.nih.gov/...",
      "source": "PubMed"
    }
  ]
}
```

For the MVP, literature retrieval should return source metadata and snippets. AI summarization should come later.

---

### `GET /api/v1/pathways`

Purpose: Return known pathways associated with a gene.

#### Query Parameters

| Parameter | Type | Required | Example |
|---|---:|---:|---|
| `gene` | string | yes | `PIK3CA` |

#### Response

```json
{
  "gene_symbol": "PIK3CA",
  "pathways": [
    {
      "name": "PI3K/AKT/mTOR signaling",
      "description": "Pathway involved in growth, survival, metabolism, and proliferation.",
      "source": "curated_static_knowledge"
    }
  ]
}
```

---

## Error Response Standard

All errors should eventually follow one standard response shape.

```json
{
  "error": {
    "code": "UNSUPPORTED_CANCER_TYPE",
    "message": "Cancer type 'x' is not currently supported.",
    "details": null
  }
}
```

Recommended error codes:

- `UNSUPPORTED_CANCER_TYPE`
- `GENE_NOT_FOUND`
- `EXTERNAL_API_FAILURE`
- `INVALID_QUERY`
- `INTERNAL_SERVER_ERROR`

---

## API Design Rules

1. Endpoints should return canonical platform objects, not raw third-party API responses.
2. Every endpoint that surfaces biomedical claims should include evidence/source information.
3. Disclaimers should be visible in both backend responses and frontend UI.
4. API naming should be explicit. Avoid vague endpoint names like `/data` once the prototype grows.
5. AI-generated summaries, if added later, must cite retrieved sources.
