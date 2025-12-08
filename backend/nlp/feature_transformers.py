# feature_transformers.py

import spacy
nlp = spacy.load("en_core_web_sm")

from nlp.keywords import (
    FR_KEYWORDS,
    ALL_NFR_KEYWORDS
)

def extract_keyword_features(text):
    text_lower = text.lower()
    features = {
        "fr_keyword_match": 0,
        "nfr_keyword_match": 0
    }

    # keyword boosting
    for kw in FR_KEYWORDS:
        if kw in text_lower:
            features["fr_keyword_match"] += 1

    for kw in ALL_NFR_KEYWORDS:
        if kw in text_lower:
            features["nfr_keyword_match"] += 1

    return features


def extract_pos_features(text):
    doc = nlp(text)
    features = {
        "num_verbs": 0,
        "num_nouns": 0,
        "num_adjectives": 0,
    }

    for token in doc:
        if token.pos_ == "VERB":
            features["num_verbs"] += 1
        if token.pos_ == "NOUN":
            features["num_nouns"] += 1
        if token.pos_ == "ADJ":
            features["num_adjectives"] += 1

    return features


def combine_features(tfidf_vector, keyword_features, pos_features):
    extra = list(keyword_features.values()) + list(pos_features.values())
    return tfidf_vector.toarray()[0].tolist() + extra
