
import random

def inject_volatility(bloom, volatility=0.1):
    # Slight mutation of existing traits
    bloom["entropy_score"] += random.uniform(-volatility, volatility)
    bloom["bloom_factor"] += random.uniform(-volatility, volatility)
    bloom["entropy_score"] = max(0.0, min(1.0, bloom["entropy_score"]))
    bloom["bloom_factor"] = max(0.5, min(2.0, bloom["bloom_factor"]))
    return bloom
