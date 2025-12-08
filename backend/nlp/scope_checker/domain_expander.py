# domain_expander.py (SMART AUTO-DOMAIN VERSION)
from typing import List, Optional
from .scope_config import ALL_UNIVERSAL_KEYWORDS  # <-- import universal keywords

DOMAIN_IDENTIFIERS = {
    "online shopping": ["shopping", "ecommerce", "store", "product", "cart", "checkout"],
    "library management": ["library", "book", "catalog", "borrow", "return"],
    "hospital management": ["hospital", "doctor", "patient", "clinic"],
    "school management": ["school", "student", "teacher", "exam"],
    "banking system": ["bank", "account", "transaction", "loan"],
}

DOMAIN_EXPANSIONS = {
    "online shopping": [
        "product", "products", "cart", "add to cart", "checkout", "payment",
        "order", "order tracking", "shipping", "delivery", "invoice",
        "login", "signup", "register", "authentication",
        "wishlist", "discount", "coupon"
    ],
    "library management": [
        "book", "isbn", "borrow", "return", "catalog",
        "reservation", "author", "publication", "librarian",
        "ebook", "digital library",
        "login", "signup", "register", "authentication"
    ],
    "hospital management": [
        "patient", "doctor", "appointment", "medicine",
        "prescription", "billing", "emergency",
        "lab report", "treatment plan",
        "login", "signup", "authentication"
    ],
    "school management": [
        "student", "teacher", "timetable", "attendance",
        "exam", "grades", "courses", "report card",
        "login", "signup", "authentication"
    ],
    "banking system": [
        "account", "transfer", "fund transfer", "balance",
        "withdraw", "deposit", "loan", "credit card",
        "login", "signup", "authentication"
    ]
}


# --------------------------------------------
# 1. SMART DOMAIN CLASSIFIER — FALLBACK DOMAIN
# --------------------------------------------
def detect_domain_category(text: str, extracted_keywords: List[str]):
    text = text.lower()
    combined = text + " " + " ".join(extracted_keywords)

    scores = {}
    for domain, ids in DOMAIN_IDENTIFIERS.items():
        scores[domain] = sum(1 for i in ids if i in combined)

    best = max(scores, key=scores.get)

    # If no domain matches → return "generic"
    return best if scores[best] > 0 else "generic"


# --------------------------------------------
# 2. SMART EXPANSION — AUTO-EXPANDS NEW DOMAINS
# --------------------------------------------
def expand_domain(base_keywords: List[str], domain: Optional[str]):
    if domain in DOMAIN_EXPANSIONS:
        # Predefined domain → merge with known expansions
        return sorted(set(base_keywords + DOMAIN_EXPANSIONS[domain]))

    # Unknown domain → auto-expand using:
    # 1. Base keywords
    # 2. Universal functional keywords (login, auth, performance, etc.)
    dynamic_expansion = base_keywords + ALL_UNIVERSAL_KEYWORDS

    return sorted(set(dynamic_expansion))
