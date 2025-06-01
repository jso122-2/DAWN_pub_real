# owl/entropy.py

def get_entropy_score(sentences):
    """
    Placeholder entropy function based on sentence variation.
    Replace with vector-based or n-gram probability logic.
    """
    if not sentences:
        return 0.0

    unique = len(set(sentences))
    total = len(sentences)
    raw_entropy = unique / total if total else 0.0
    return round(raw_entropy, 3)
