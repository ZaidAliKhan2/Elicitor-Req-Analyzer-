# scope_manager.py
import re
from .domain_extractor import extract_domain_keywords
from .domain_expander import expand_domain, detect_domain_category
from .scope_similarity import compute_similarity, compute_keyword_overlap
from .scope_config import ALL_UNIVERSAL_KEYWORDS


def build_strict_pattern(keyword: str):
    """
    Creates a strict regex pattern:
    - Exact whole word match
    - Multi-word phrase match
    - No substring matching
    """
    escaped = re.escape(keyword)
    if " " in keyword:
        return re.compile(rf"\b{escaped}\b", re.IGNORECASE)
    else:
        return re.compile(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", re.IGNORECASE)


# Precompile universal keyword patterns (FAST!)
UNIVERSAL_PATTERNS = [
    (kw, build_strict_pattern(kw))
    for kw in ALL_UNIVERSAL_KEYWORDS
]


class ScopeManager:
    def __init__(self, threshold=0.40):
        self.threshold = threshold
        self.domain_keywords = []
        self.domain = None

    def set_project_description(self, text: str):
        base = extract_domain_keywords(text)
        self.domain = detect_domain_category(text, base)
        self.domain_keywords = expand_domain(base, self.domain)

        return {
            "base_keywords": base,
            "expanded_keywords": self.domain_keywords,
            "domain": self.domain
        }

    def check_scope(self, requirement: str):
        req_lower = requirement.lower()

        # STRICT UNIVERSAL REQUIREMENT CHECK
        for keyword, pattern in UNIVERSAL_PATTERNS:
            if pattern.search(req_lower):
                return {
                    "in_scope": True,
                    "confidence": 0.95,
                    "similarity": 1.0,
                    "overlap": 1.0,
                    "reason": f"Universal requirement detected ('{keyword}') – valid for all domains"
                }

        # DOMAIN-BASED CHECK (fallback)
        sim = compute_similarity(requirement, self.domain_keywords)
        overlap = compute_keyword_overlap(requirement, self.domain_keywords)
        score = (0.7 * sim) + (0.3 * overlap)

        return {
            "in_scope": score >= self.threshold,
            "similarity": sim,
            "overlap": overlap,
            "confidence": score,
            "reason": self._reason(score, sim)
        }

    def _reason(self, score, sim):
        if score >= self.threshold:
            return "Relevant to project scope"
        if sim < 0.2:
            return "Low semantic relevance"
        return "Partially related but outside project scope"
