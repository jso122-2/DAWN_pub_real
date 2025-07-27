
# Sigil-linked symbolic constants, variables, and formula maps

SIGIL_VARIABLES = {
    "SCUP": "Semantic Coherence Under Pressure",
    "TP-RAR": "Task Pressure – Recency Adjusted Relevance",
    "E_s": "Sigil entropy (active sigils / capacity)",
    "V_e": "Edge volatility (tracked via Beetle)",
    "D_t": "Tracer divergence (conflict across agents)",
    "S_c": "Current SCUP value",
    "SHI": "Schema Health Index",
    "A": "Ash yield",
    "T": "Ticks at SCUP ≥ 0.9",
    "λ": "Nutrient decay rate",
    "N_t": "Nutrient strength at tick t",
    "CMS": "Context Match Score (absorbed into TP-RAR)",
    "θ": "Sigil temperature decay bias",
    "η": "Pressure decay constant",
    "w_h": "Weight of house impact on SCUP",
    "T_{edge}": "Soft edge tension (0–1)",
    "ΔT": "Tension delta over ticks",
    "k": "Ash acceleration constant",
    "W_r": "TP-RAR recency weight",
    "W_p": "TP-RAR pressure weight"
}

SIGIL_FORMULAE = {
    "SCUP": "SCUP = (S_i * TP-RAR) / (1 + P_s + U_p)",
    "TP-RAR": "TP-RAR = (R * W_r) + (P * W_p)",
    "SHI": "SHI = 1 - (α·E_s + β·V_e + γ·D_t + δ·(1 - S_c) + ε·(Soot / (Ash + 1)))",
    "NutrientDecay": "N_{t+1} = N_t * λ",
    "AshYield": "A = A_base * e^(k * (T - T_min))",
    "EdgeVolatility": "V = std(ΔT_{edge}) + avg(|ΔT_{edge}|) * W",
    "SigilDecay": "Decay_h = θ * T_temp + η * P_h"
}

# Formula rendering logic

def get_formula_description(key):
    name = SIGIL_VARIABLES.get(key, "Unknown Variable")
    formula = SIGIL_FORMULAE.get(key, "No formula defined")
    return f"{key}: {name} — {formula}"
