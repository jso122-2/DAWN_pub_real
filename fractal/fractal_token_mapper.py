# fractal_token_mapper.py
# 🔧 Stub for semantic recursion depth mapping

def map_tokens_to_depths(words: list[str]) -> list[int]:
    """
    Maps each word to a recursion depth using vowel richness.
    Ensures every token has at least depth 1.
    """
    return [sum(1 for c in word.lower() if c in 'aeiou') or 1 for word in words]

# Example usage:
if __name__ == "__main__":
    tokens = ["semantic", "recursion", "field", "pressure"]
    depths = map_tokens_to_depths(tokens)
    print(f"Tokens: {tokens}\nDepths: {depths}")
