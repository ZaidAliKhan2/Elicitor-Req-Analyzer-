"""
requirement_analyzer.py
Unified Requirement Analyzer
Combines scope checking and FR/NFR classification
"""

import numpy as np
# requirement_analyzer.py (TOP OF FILE)

import os
import pickle
from typing import Dict, List, Optional, Tuple

# -------------------------
# FIXED IMPORTS (100% CORRECT)
# -------------------------

# Add backend to PYTHONPATH
import sys
sys.path.append(os.path.dirname(__file__))

# Import scope checker
from nlp.scope_checker.scope_manager import ScopeManager

# Import feature transformers
from nlp.feature_transformers import extract_keyword_features, extract_pos_features


ModelTuple = Tuple[object, object]  # (vectorizer, model)


class RequirementAnalyzer:
    """
    Unified analyzer that checks scope and classifies requirements
    """

    def __init__(self,
                 project_description: Optional[str] = None,
                 scope_threshold: float = 0.40,
                 fr_nfr_model_path: str = "backend/models/fr_nfr_model.pkl",
                 nfr_sub_model_path: str = "backend/models/nfr_sub_model.pkl"):
        """
        Args:
            project_description: initial project description to set scope
            scope_threshold: threshold passed to ScopeManager (confidence cutoff)
            fr_nfr_model_path: path to pickled (vectorizer, model) for FR/NFR
            nfr_sub_model_path: path to pickled (vectorizer, model) for NFR subcategories
        """
        # Initialize scope manager
        self.scope_manager = ScopeManager(threshold=scope_threshold)

        # If a project description was provided, initialize scope
        if project_description:
            self.scope_manager.set_project_description(project_description)

        # Load models (expecting pickle of (vectorizer, model))
        self.fr_nfr_model: Optional[ModelTuple] = None
        self.nfr_sub_model: Optional[ModelTuple] = None

        if fr_nfr_model_path and os.path.exists(fr_nfr_model_path):
            loaded = self._load_model(fr_nfr_model_path)
            if loaded:
                self.fr_nfr_model = loaded
                print(f"✅ FR/NFR model loaded from: {fr_nfr_model_path}")
        else:
            print(f"⚠️  FR/NFR model NOT FOUND at {fr_nfr_model_path}")

        if nfr_sub_model_path and os.path.exists(nfr_sub_model_path):
            loaded = self._load_model(nfr_sub_model_path)
            if loaded:
                self.nfr_sub_model = loaded
                print(f"✅ NFR sub-category model loaded from: {nfr_sub_model_path}")
        else:
            print(f"⚠️  NFR sub-category model NOT FOUND at {nfr_sub_model_path}")

   
   
    def _load_model(self, path: str) -> Optional[ModelTuple]:
        """
        Load a pickled (vectorizer, model) tuple or a raw model.
        Returns (vectorizer, model) or None on error.
        """
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
            # If it's a tuple (vectorizer, model) keep it
            if isinstance(obj, tuple) and len(obj) == 2:
                return obj
            # If it's a plain model (rare in your pipeline), return (None, model)
            return (None, obj)
        except Exception as e:
            print(f"Error loading model from {path}: {e}")
            return None

    def _transform_with_custom_features(self, texts, vectorizer):
       """Match training pipeline: TF-IDF + keyword + POS features"""
       tfidf_features = vectorizer.transform(texts)

       combined = []
       for i, text in enumerate(texts):
           tfidf_row = tfidf_features[i].toarray()[0].tolist()

           keyword_feats = extract_keyword_features(text)
           pos_feats = extract_pos_features(text)

           extras = list(keyword_feats.values()) + list(pos_feats.values())
 
           combined.append(tfidf_row + extras)

       return np.array(combined)

    # -------------------------
    # Public API
    # -------------------------
    def analyze_requirement(self, requirement: str) -> Dict:
        """
        Analyze a single requirement for both scope and classification.
        Returns a dictionary shaped for your tester.
        """
        result = {
            "requirement": requirement,
            "scope_check": {},
            "classification": {},
            "overall_status": None
        }

        # 1) Scope check
        scope_result = self._check_scope(requirement)
        result["scope_check"] = scope_result

        # 2) Classification only if in scope
        if scope_result.get("in_scope"):
            classification_result = self._classify_requirement(requirement)
            result["classification"] = classification_result
            result["overall_status"] = "ANALYZED"
        else:
            result["classification"] = {
                "type": "NOT_APPLICABLE",
                "confidence": 0.0,
                "reason": "Out of scope"
            }
            result["overall_status"] = "OUT_OF_SCOPE"

        return result

    def analyze_batch(self, requirements: List[str]) -> List[Dict]:
        return [self.analyze_requirement(r) for r in requirements]

    def get_summary_statistics(self, results: List[Dict]) -> Dict:
        total = len(results)
        in_scope = sum(1 for r in results if r["scope_check"].get("in_scope"))
        out_of_scope = total - in_scope
        fr_count = sum(1 for r in results if r["classification"].get("type") == "FR")
        nfr_count = sum(1 for r in results if r["classification"].get("type") == "NFR")

        nfr_subs = {}
        for r in results:
            if r["classification"].get("type") == "NFR":
                sub = r["classification"].get("sub_category", "Unknown")
                nfr_subs[sub] = nfr_subs.get(sub, 0) + 1

        return {
            "total_requirements": total,
            "in_scope": in_scope,
            "out_of_scope": out_of_scope,
            "functional_requirements": fr_count,
            "non_functional_requirements": nfr_count,
            "nfr_subcategories": nfr_subs,
            "scope_percentage": (in_scope / total * 100) if total else 0,
            "fr_percentage": (fr_count / in_scope * 100) if in_scope else 0,
            "nfr_percentage": (nfr_count / in_scope * 100) if in_scope else 0,
        }

    # -------------------------
    # Internal helpers
    # -------------------------
    def _check_scope(self, requirement: str) -> Dict:
        """
        Use scope_manager.check_scope and map to expected tester structure.
        Also returns similarity scores map (simple: only one domain in your current manager).
        """
        scope_res = self.scope_manager.check_scope(requirement)

        similarity_scores = {}
        if self.scope_manager.domain is not None:
            similarity_scores[self.scope_manager.domain] = scope_res.get("similarity", 0.0)

        return {
            "in_scope": scope_res.get("in_scope", False),
            "matched_domains": [self.scope_manager.domain] if scope_res.get("in_scope") and self.scope_manager.domain else [],
            "similarity_scores": similarity_scores,
            "best_match": self.scope_manager.domain if scope_res.get("in_scope") else self.scope_manager.domain,
            "best_score": scope_res.get("confidence", 0.0),
            "threshold": self.scope_manager.threshold,
            "message": scope_res.get("reason", "")
        }

    def _classify_requirement(self, requirement: str) -> Dict:
       if not self.fr_nfr_model:
        return {
            "type": "UNKNOWN",
            "confidence": 0.0,
            "sub_category": None,
            "message": "FR/NFR classification model not loaded"
        }

       vectorizer, model = self.fr_nfr_model

       try:
         # FIX: Apply SAME training pipeline → TF-IDF + Keyword + POS
         X = self._transform_with_custom_features([requirement], vectorizer)

         pred = model.predict(X)[0]
 
         confidence = 0.0
         if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0]
            confidence = float(max(proba))

         sub_category = None
         if pred == "NFR":
            sub_category = self._determine_nfr_subcategory(requirement)

         return {
            "type": pred,
            "confidence": confidence,
            "sub_category": sub_category,
            "message": f"Classified as {pred}"
        }

       except Exception as e:
        return {
            "type": "ERROR",
            "confidence": 0.0,
            "sub_category": None,
            "message": f"Classification error: {e}"
        }

    def _determine_nfr_subcategory(self, requirement: str) -> str:
        """
        Prefer the trained NFR sub-model if available; otherwise use a keyword fallback.
        """
        # If we have a trained NFR sub-model, use it
        if self.nfr_sub_model:
            vec, model = self.nfr_sub_model
            try:
                if vec is not None:
                    X = self._transform_with_custom_features([requirement], vec)
                else:
                    X = [requirement]
                return model.predict(X)[0]
            except Exception:
                # Fall through to keyword fallback
                pass

        # Keyword fallback (simple, strict substring checks are fine here)
        req_lower = requirement.lower()
        nfr_categories = {
            "Performance": ["performance", "speed", "response time", "latency", "throughput"],
            "Security": ["security", "encrypt", "encryption", "authentication", "authorization", "privacy"],
            "Usability": ["usability", "user-friendly", "intuitive", "accessible", "ux", "ui"],
            "Reliability": ["reliability", "uptime", "backup", "restore", "failover"],
            "Scalability": ["scalability", "scale", "concurrent", "concurrent users", "load"],
            "Maintainability": ["maintainability", "refactor", "modular", "documentation"]
        }

        for cat, kws in nfr_categories.items():
            for kw in kws:
                if kw in req_lower:
                    return cat

        return "General"
