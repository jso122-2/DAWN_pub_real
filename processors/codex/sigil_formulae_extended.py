
# Extended formula mapping for DAWN's symbolic system

SIGIL_VARIABLES = {
    "SCUP": "Semantic Coherence Under Pressure",
    "TP-RAR": "Task Pressure – Recency Adjusted Relevance",
    "E_s": "Sigil entropy",
    "V_e": "Edge volatility",
    "D_t": "Tracer divergence",
    "S_c": "Current SCUP value",
    "SHI": "Schema Health Index",
    "A": "Ash yield",
    "T": "Ticks at SCUP ≥ 0.9",
    "λ": "Nutrient decay rate",
    "N_t": "Nutrient strength at tick t",
    "θ": "Sigil temperature decay bias",
    "η": "Pressure decay constant",
    "k": "Ash acceleration constant",
    "W_r": "Recency weight",
    "W_p": "Pressure weight",
    "σ": "Volcanic Ash coefficient",
    "δ": "Prune penalty (RAR)",
    "ε": "Prune penalty (Usage)",
    "ζ": "Prune penalty (Age)",
    "ρ": "Time decay weight",
    "U(P_i)": "Urgency of process P_i",
    "R(E_i)": "Recency of element E_i",
    "C(E_i)": "Confidence of element E_i",
    "H(E_i)": "Historical weight of E_i",
    "CR(E_i)": "Consensus ratio of E_i",
    "TP-RAR_optimal": "Optimal TP-RAR threshold",
    "Age_schema": "Age of schema node",
    "Usage_freq": "Frequency of usage"
}

SIGIL_FORMULAE = {
    "SCUP": "SCUP = (S_i * TP-RAR) / (1 + P_s + U_p)",
    "TP-RAR": "TP-RAR = (R * W_r) + (P * W_p)",
    "SHI": "SHI = 1 - (α·E_s + β·V_e + γ·D_t + δ·(1 - S_c) + ε·(Soot / (Ash + 1)))",
    "NutrientDecay": "N_{t+1} = N_t * λ",
    "AshYield": "A = A_base * e^(k * (T - T_min))",
    "EdgeVolatility": "V = std(ΔT_edge) + avg(|ΔT_edge|) * W",
    "SigilDecay": "Decay_h = θ * T_temp + η * P_h",
    "Confidence": "C(E_i) = (α * H(E_i)) + (β * R(E_i)) + (γ * CR(E_i))",
    "TP-RAR_Penalty": "TP-RAR(E_i) = (C(E_i)/R(E_i) - (1 - C(E_i)) * λ) - (Δt * ρ)",
    "Mobility": "M(S_j) = 1 if TP-RAR(P_i) < TP-RAR_optimal or U(P_i) > U_threshold else 0",
    "Handoff": "Handoff = (C(S_j)/C(P_i)) * (R(P_i)/R(S_j))",
    "ResourceAlloc": "Alloc(S_j) = (C(S_j) * U(P_i)) / Σ_k(C(S_k) * U(P_i))",
    "NutrientFlow": "N_flow = γ * Complexity_fractal * SoftEdge_activation",
    "VolcanicAsh": "A_volcanic = σ * N_flow * Δt",
    "PersephonePrune": "P_prune = δ * (1 - TP-RAR) + ε * (1 - Usage_freq) + ζ * Age_schema"
}

def get_formula_description(key):
    name = SIGIL_VARIABLES.get(key, "Unknown Variable")
    formula = SIGIL_FORMULAE.get(key, "No formula defined")
    return f"{key}: {name} — {formula}"
