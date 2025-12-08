import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

from feature_transformers import extract_keyword_features, extract_pos_features, combine_features

TRAIN_FILE = "data/nfr_sub_allcat_train.txt"
MODEL_PATH = "backend/models/nfr_sub_model.pkl"

def load_data(path):
    labels, texts = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            label, text = line.strip().split(" ", 1)
            labels.append(label.replace("__label__", "").strip())
            texts.append(text)
    return texts, labels

print("Loading NFR subcategory data...")
X_raw, y = load_data(TRAIN_FILE)

vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=7000)
X_tfidf = vectorizer.fit_transform(X_raw)

X_final = []

for i, text in enumerate(X_raw):
    kw = extract_keyword_features(text)
    pos = extract_pos_features(text)
    combined = combine_features(X_tfidf[i], kw, pos)
    X_final.append(combined)

X_final = np.array(X_final)

model = LogisticRegression(max_iter=1200)
model.fit(X_final, y)

with open(MODEL_PATH, "wb") as f:
    pickle.dump((vectorizer, model), f)

print("NFR Subcategory Model trained successfully!")
