import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

vectorizer = HashingVectorizer(n_features=256, norm="l2", alternate_sign=False)


def embed_text(text: str) -> list[float]:
    vec = vectorizer.transform([text]).toarray().astype(np.float32)[0]
    return vec.tolist()
