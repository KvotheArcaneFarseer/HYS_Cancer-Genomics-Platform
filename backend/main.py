from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from services.cbioportal import fetch_cancer_profile

app = FastAPI(title="Cancer Genomics Research API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data")
def get_cancer_profile(cancer_type: str = Query(... ), gene: str = Query(...)):
    
    data = fetch_cancer_profile(cancer_type, gene)
    if data is None:
        return {"error": f"Cancer type '{cancer_type}' is not supported yer."}
    return data

@app.get("/health")
def health():
    return {"status": "ok"}