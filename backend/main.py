from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="Cancer Genomics Research API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)

@app.get("/data")
def get_cancer_profile(cancer_type: str = Query(... ), gene: str = Query(...)):
    # Day 1 task: return mock data
    mock_path = os.path.join(BASE_DIR, "Mock_cancer_profile.json")
    with open(mock_path) as f:
        data = json.load(f)
    return data

@app.get("/health")
def health():
    return {"status": "ok"}