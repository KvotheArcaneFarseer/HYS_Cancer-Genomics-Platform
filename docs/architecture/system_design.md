# System Design

## Project Identity

**Project name:** HYS Cancer Genomics Platform  
**Current product direction:** Cancer Genomics Research Intelligence Platform  
**Purpose:** Research and education tool for exploring cancer genomics evidence.  
**Non-goal:** This is not a diagnostic, prognostic, or treatment recommendation system.

The platform should help users connect cancer type, genes, mutations, mutation frequency, biological pathways, public datasets, literature, and eventually therapy-related evidence. The system should make evidence easier to explore without pretending to replace clinicians or molecular tumor boards.

---

## Current MVP

The current MVP already demonstrates the first vertical slice:

```text
cBioPortal dataset → FastAPI backend → Streamlit frontend
```

Current user flow:

1. User selects a cancer type.
2. User enters a gene symbol.
3. Frontend calls the backend `/data` endpoint.
4. Backend queries cBioPortal.
5. Backend returns mutation frequency and common mutations.
6. Frontend displays summary metrics and a mutation chart/table.

This proves the basic architecture works, but it is not yet a full intelligence platform. It is currently closer to a mutation frequency lookup dashboard.

---

## Architectural Principles

### 1. Data before AI

The platform should retrieve and structure reliable evidence before any generative AI is introduced.

Preferred pipeline:

```text
Public datasets
    ↓
Data normalization
    ↓
Knowledge layer
    ↓
Evidence retrieval
    ↓
Optional AI summarization
    ↓
Frontend display
```

The AI layer, if added later, should summarize retrieved evidence only. It should not be treated as the source of truth.

### 2. Separate integrations from business logic

External APIs should live in integration modules. Higher-level reasoning and aggregation should live in service modules.

Example:

```text
integrations/cbioportal.py  → talks to cBioPortal only
services/gene_service.py    → combines cBioPortal, pathway, literature, and therapy data
api/routes.py               → exposes clean API endpoints
```

### 3. Define canonical internal data models

External APIs use inconsistent field names. The backend should normalize everything into platform-specific models before sending responses to the frontend.

Example canonical object:

```text
GeneProfile
├── gene_symbol
├── cancer_type
├── study_id
├── mutation_frequency
├── common_mutations
├── biological_function
├── affected_pathways
├── targeted_therapies
├── literature
└── evidence_sources
```

### 4. Keep the frontend simple until the backend is stable

The frontend should visualize and explain backend outputs. It should not contain biomedical logic.

---

## Proposed Backend Structure

```text
backend/
├── main.py
├── api/
│   ├── __init__.py
│   └── routes.py
├── integrations/
│   ├── __init__.py
│   ├── cbioportal.py
│   ├── pubmed.py
│   └── pathway_sources.py
├── services/
│   ├── __init__.py
│   ├── gene_service.py
│   ├── cancer_service.py
│   └── literature_service.py
├── schemas/
│   ├── __init__.py
│   └── gene_profile.py
├── data/
│   └── static_gene_knowledge.json
├── utils/
│   ├── __init__.py
│   └── errors.py
└── tests/
    ├── test_health.py
    └── test_gene_profile.py
```

Current repository state is simpler than this. Refactoring toward this structure should be done gradually, not all at once.

---

## Proposed Frontend Structure

```text
frontend/
├── app.py
├── components/
│   ├── gene_summary.py
│   ├── mutation_metrics.py
│   └── literature_table.py
└── requirements.txt
```

For now, Streamlit is appropriate because it enables fast dashboard development. React should only be considered once the core product direction is clearer.

---

## System Components

### Frontend

Responsibilities:

- Collect cancer type and gene input.
- Call backend endpoints.
- Display mutation metrics.
- Display gene function, pathways, literature, and therapy evidence when available.
- Show disclaimers clearly.

The frontend should not directly call cBioPortal, PubMed, or other scientific databases.

### API Layer

Responsibilities:

- Define endpoints.
- Validate user input.
- Call service layer.
- Return consistent JSON responses.
- Handle expected errors cleanly.

### Service Layer

Responsibilities:

- Combine data from multiple sources.
- Apply platform-level logic.
- Build canonical response objects.
- Avoid exposing raw third-party API responses directly.

### Integration Layer

Responsibilities:

- Call external data sources.
- Translate raw API responses into intermediate forms.
- Handle request failures and API-specific quirks.

### Knowledge Layer

Responsibilities:

- Store curated disease/gene/pathway knowledge.
- Provide plain-language summaries.
- Provide source references.
- Eventually support retrieval-augmented generation.

---

## Immediate Technical Gaps

1. Biological function fields are placeholders.
2. Pathway data is not implemented.
3. Literature retrieval is not implemented.
4. Targeted therapy evidence is not implemented.
5. Error handling around invalid genes/API failures is too thin.
6. Cancer types are hardcoded.
7. Tests are missing.
8. Backend package structure needs cleanup before complexity grows.

---

## Next Architecture Step

The next best engineering move is to add a **Gene Knowledge Engine**.

It should provide:

- Gene description
- Biological function
- Affected pathways
- Cancer relevance
- Evidence/source links

This should be implemented first using structured/static data, not generative AI.
