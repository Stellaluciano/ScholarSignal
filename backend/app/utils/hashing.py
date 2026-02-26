import hashlib


def fingerprint_paper(title: str, authors: list[str]) -> str:
    return hashlib.sha256(f"{title}|{'|'.join(authors)}".encode()).hexdigest()
