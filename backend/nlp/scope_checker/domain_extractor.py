# domain_extractor.py  (STABLE VERSION)
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

STOP_WORDS = {
    "system", "software", "application", "project", "platform",
    "user", "allow", "enable", "provide", "make", "create",
    "build", "develop", "feature", "functionality"
}

def extract_domain_keywords(text: str):
    doc = nlp(text.lower())
    keywords = set()

    for chunk in doc.noun_chunks:
        c = chunk.text.strip()
        if len(c) < 3: continue
        if all(w in STOP_WORDS for w in c.split()): continue
        keywords.add(c)

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            if token.lemma_ not in STOP_WORDS:
                keywords.add(token.lemma_.lower())

    cleaned = sorted(set(k.strip() for k in keywords if len(k.strip()) > 2))
    return cleaned
