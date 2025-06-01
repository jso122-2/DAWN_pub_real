def owl_adjust_weights(entropy_log, scup_history):
    """
    Owl's memory-based override on dynamic weights.
    If entropy is rising and SCUP is falling, boost ENTROPY weight.
    """
    if len(entropy_log) < 3 or len(scup_history) < 3:
        return None

    avg_entropy = sum(entropy_log[-3:]) / 3
    scup_drop = scup_history[-2] - scup_history[-1]

    weights = {}
    if scup_drop > 0.05 and avg_entropy > 0.4:
        weights["W_ENTROPY"] = 2.0
        weights["W_TP"] = 0.8
        weights["W_URGENCY"] = 1.2
        weights["W_PRESSURE"] = 1.1
        return weights

    return None
