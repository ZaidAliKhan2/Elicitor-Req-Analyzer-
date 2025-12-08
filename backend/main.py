# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import traceback

# Import your analyzer (assumes backend/requirement_analyzer.py exists and imports local nlp package)
try:
    from backend.requirement_analyzer import RequirementAnalyzer
except Exception:
    # fallback when running as "python backend/main.py" (module path differences)
    from requirement_analyzer import RequirementAnalyzer  # type: ignore

app = FastAPI(title="Elicitor - Requirement Analyzer API", version="0.1")

# Allow CORS for local dev (adapt origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your UI origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- request models ---
class ProjectInit(BaseModel):
    project_description: str
    scope_threshold: Optional[float] = 0.40

class SingleReq(BaseModel):
    requirement: str

class BatchReq(BaseModel):
    requirements: List[str]

# --- global analyzer instance ---
ANALYZER: Optional[RequirementAnalyzer] = None

# Helper for instantiating analyzer
def create_analyzer(project_description: Optional[str] = None, scope_threshold: float = 0.40,
                    fr_nfr_model_path: str = "backend/models/fr_nfr_model.pkl",
                    nfr_sub_model_path: str = "backend/models/nfr_sub_model.pkl") -> RequirementAnalyzer:
    # Instantiate RequirementAnalyzer from your file
    return RequirementAnalyzer(
        project_description=project_description,
        scope_threshold=scope_threshold,
        fr_nfr_model_path=fr_nfr_model_path,
        nfr_sub_model_path=nfr_sub_model_path
    )

# --- endpoints ---
@app.get("/")
def root():
    return {"service": "Elicitor Requirement Analyzer", "status": "ok"}

@app.post("/init_project")
def init_project(payload: ProjectInit):
    global ANALYZER
    try:
        ANALYZER = create_analyzer(
            project_description=payload.project_description,
            scope_threshold=payload.scope_threshold
        )
        return {"ok": True, "message": "Project initialized", "domain": ANALYZER.scope_manager.domain}
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Init failed: {e}\n{tb}")

@app.post("/analyze")
def analyze_single(payload: SingleReq):
    global ANALYZER
    if ANALYZER is None:
        raise HTTPException(status_code=400, detail="Project not initialized. Please call /init_project first.")
    try:
        res = ANALYZER.analyze_requirement(payload.requirement)
        return {"ok": True, "result": res}
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Analyze failed: {e}\n{tb}")

@app.post("/analyze_batch")
def analyze_batch(payload: BatchReq):
    global ANALYZER
    if ANALYZER is None:
        ANALYZER = create_analyzer()
    try:
        results = ANALYZER.analyze_batch(payload.requirements)
        summary = ANALYZER.get_summary_statistics(results)
        return {"ok": True, "results": results, "summary": summary}
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Batch analyze failed: {e}\n{tb}")

@app.get("/models_status")
def models_status():
    """
    Report which models were loaded (quick health check).
    """
    global ANALYZER
    status = {
        "analyzer_initialized": ANALYZER is not None,
        "fr_nfr_model_loaded": False,
        "nfr_sub_model_loaded": False,
        "model_paths": {
            "fr_nfr": "backend/models/fr_nfr_model.pkl",
            "nfr_sub": "backend/models/nfr_sub_model.pkl"
        }
    }
    if ANALYZER:
        status["fr_nfr_model_loaded"] = ANALYZER.fr_nfr_model is not None
        status["nfr_sub_model_loaded"] = ANALYZER.nfr_sub_model is not None
    return status

