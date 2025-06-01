# router.py


def route_decision(pulse, seed: str) -> str:
    """
    Decide which model to route the seed to based on its trust score.
    """
    trust = pulse.get_trust_score(seed)

    if trust > 0.75:
        model = "gpt-4o"  # ✅ fast & trusted
    elif trust > 0.4:
        model = "gpt-4"   # 🧠 deeper reflection
    else:
        model = "blocked"  # ⚠️ schema considers this untrustworthy

    print(f"[Router] 🗭 Trust score for {seed}: {trust} → Routing to {model}")
    return model
