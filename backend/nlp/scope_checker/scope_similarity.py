# scope_similarity.py
from sentence_transformers import SentenceTransformer, util
import numpy as np
import math

# Load model once
MODEL_NAME = "all-MiniLM-L6-v2"
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def compute_similarity(requirement: str, project_keywords: list) -> float:
    """
    Compute a single semantic similarity score between requirement and project scope.
    We produce a single embedding for the project (mean of keyword embeddings)
    and compare it to the requirement embedding.

    Returns a float between 0.0 and 1.0
    """
    model = _get_model()

    if not project_keywords:
        return 0.0

    # If project_keywords is a long list, join in small chunks to avoid memory issues
    # Build embeddings for keywords and take mean
    kw_texts = [str(k) for k in project_keywords if k and isinstance(k, str)]
    if not kw_texts:
        return 0.0

    # Encode keywords (batch)
    kw_embs = model.encode(kw_texts, convert_to_tensor=True, show_progress_bar=False)
    # mean embedding
    proj_emb = kw_embs.mean(dim=0, keepdim=True)

    # requirement embedding
    req_emb = model.encode(requirement, convert_to_tensor=True, show_progress_bar=False).unsqueeze(0)

    # cosine similarity -> tensor [1,1]
    cos = util.cos_sim(proj_emb, req_emb)
    # convert to float safely
    try:
        sim = float(cos.cpu().numpy().item())
    except Exception:
        # fallback: compute with numpy
        sim = float(np.dot(proj_emb.cpu().numpy().ravel(), req_emb.cpu().numpy().ravel()) /
                    (np.linalg.norm(proj_emb.cpu().numpy()) * np.linalg.norm(req_emb.cpu().numpy()) + 1e-9))
    # clamp
    sim = max(0.0, min(1.0, sim))
    return sim

def compute_keyword_overlap(requirement: str, project_keywords: list) -> float:
    """
    Return normalized overlap score between 0 and 1:
    number_of_matching_keywords / total_project_keywords
    """
    if not project_keywords:
        return 0.0

    req = requirement.lower()
    # simple matching: check keyword presence in requirement text
    matches = 0
    for kw in project_keywords:
        if not isinstance(kw, str):
            continue
        k = kw.lower().strip()
        if not k:
            continue
        # match multi-word and single-word; basic containment check
        if k in req:
            matches += 1
        else:
            # try token-level matching for single words
            words = k.split()
            if all(w in req for w in words):
                matches += 1

    denom = max(1, len(project_keywords))
    return matches / denom
