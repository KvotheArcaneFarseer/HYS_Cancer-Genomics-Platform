# Project Roadmap

## Project Direction

The project should evolve from a working hackathon demo into a structured cancer genomics research platform.

The current repository already contains a useful foundation:

```text
cBioPortal → FastAPI backend → Streamlit frontend
```

The roadmap below prevents the project from becoming a messy collection of disconnected features.

---

## Current State

### Completed

- FastAPI backend skeleton.
- `/health` endpoint.
- `/data` endpoint.
- cBioPortal integration.
- Breast cancer and lung adenocarcinoma study mappings.
- Mutation frequency calculation.
- Common mutation extraction.
- Streamlit frontend.
- User input for cancer type and gene symbol.
- Mutation metrics display.
- Top mutation chart/table.
- Research-only disclaimer.

### Current Weakness

The application currently shows mutation frequency and common mutations, but the interpretation layer is still missing.

It does not yet explain:

- What the gene does.
- Why the gene matters in cancer.
- Which pathways are affected.
- Which papers support the claim.
- Which therapies or therapy classes are connected to the gene.

---

## Milestone 1 — Stabilize Current MVP

### Goal

Make the existing backend/frontend pipeline reliable and clean.

### Tasks

- Refactor backend into clearer modules.
- Rename `/data` or add `/api/v1/gene-profile`.
- Add consistent error handling.
- Add response schemas with Pydantic.
- Add tests for `/health` and gene profile behavior.
- Improve README instructions.

### Success Criteria

A user can run the project locally and reliably query `Breast + TP53` or `Lung + EGFR` without confusing errors.

---

## Milestone 2 — Gene Knowledge Engine

### Goal

Turn the app from a mutation counter into a basic genomics explanation tool.

### Tasks

- Create `static_gene_knowledge.json`.
- Add curated gene summaries.
- Add affected pathway list.
- Add cancer relevance text.
- Add source fields.
- Display this information in the frontend.

### Initial Genes

- `TP53`
- `PIK3CA`
- `BRCA1`
- `BRCA2`
- `EGFR`
- `ALK`

### Success Criteria

For `Breast + TP53`, the platform returns mutation frequency plus a plain-language explanation of TP53, pathways, and cancer relevance.

---

## Milestone 3 — Literature Retrieval

### Goal

Add evidence retrieval from scientific literature.

### Tasks

- Add PubMed/NCBI E-utilities integration.
- Search by cancer type + gene.
- Return titles, authors, year, journal, abstract snippet, and PubMed links.
- Add frontend literature section.

### Non-Goal

Do not add generative AI summarization yet.

### Success Criteria

For `TP53 breast cancer`, the platform displays several relevant papers with metadata and links.

---

## Milestone 4 — Pathway Expansion

### Goal

Make the platform biologically richer by showing pathway-level context.

### Tasks

- Add curated pathway descriptions.
- Optionally integrate Reactome later.
- Show pathway names and descriptions in frontend.
- Connect genes to pathway-level cancer mechanisms.

### Success Criteria

For `PIK3CA`, the platform explains PI3K/AKT/mTOR signaling and why pathway dysregulation matters in cancer.

---

## Milestone 5 — Better Research Dashboard

### Goal

Improve frontend usability and demo quality.

### Tasks

- Add layout sections:
  - Gene overview
  - Mutation frequency
  - Common mutations
  - Pathways
  - Literature
  - Evidence sources
- Add clearer disclaimers.
- Add exportable report option.
- Add better charts.

### Success Criteria

The project feels like a coherent research dashboard, not just a Streamlit form.

---

## Milestone 6 — RAG / AI Summary Layer

### Goal

Add AI only after retrieval is stable.

### Architecture

```text
User query
    ↓
Retrieve structured data and papers
    ↓
Pass retrieved evidence to LLM
    ↓
Generate cited summary
    ↓
Show sources
```

### Rules

- AI must summarize retrieved evidence only.
- AI output must include citations or source references.
- AI must not generate treatment recommendations.
- AI summaries should be optional, not required for the core app to function.

### Success Criteria

The system can summarize retrieved literature in a controlled, citation-aware way.

---

## Milestone 7 — Precision Oncology Expansion

### Goal

Expand from gene-level exploration to more advanced precision oncology research features.

### Possible Features

- Multi-gene profiles.
- Cohort comparison.
- Patient similarity search using public cohorts.
- Drug evidence ranking.
- Clinical trial matching.
- Multi-omics integration.
- Explainable machine learning.

### Caution

This phase must maintain the research-only framing. Do not present outputs as medical recommendations.

---

## Near-Term Priority Order

The next 5 work items should be:

1. Add backend package structure gradually.
2. Add canonical Pydantic response schema for gene profiles.
3. Add static curated gene knowledge file.
4. Merge cBioPortal mutation data with gene knowledge data.
5. Update frontend to show biological function/pathways.

Do not jump to AI summaries or clinical trial matching yet.

---

## Demo Strategy

The best demo path is narrow and polished:

```text
Breast Cancer + TP53
```

The demo should show:

- Mutation frequency from cBioPortal.
- Common mutations.
- Biological function.
- Affected pathways.
- Cancer relevance.
- Literature links later.
- Clear research-only disclaimer.

If this single flow works well, expansion to additional cancers and genes becomes much easier.
