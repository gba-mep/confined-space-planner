"""
risk_calculator.py — Step 2: Risk matrix calculation (Severity × Likelihood).
=========================================================================
Implements ISO 31000 risk assessment framework.
"""

SEVERITY_LEVELS = {
    5: {"label": "Catastrophic", "desc": "Death or permanent disability"},
    4: {"label": "Severe", "desc": "Serious injury requiring hospitalization"},
    3: {"label": "Moderate", "desc": "Injury requiring medical treatment"},
    2: {"label": "Minor", "desc": "Minor injury, self-treatable"},
    1: {"label": "Negligible", "desc": "No injury, property damage only"},
}

LIKELIHOOD_LEVELS = {
    5: {"label": "Almost Certain", "desc": "Could happen in most circumstances"},
    4: {"label": "Likely", "desc": "Will probably occur"},
    3: {"label": "Possible", "desc": "Might occur occasionally"},
    2: {"label": "Unlikely", "desc": "Could happen but rarely"},
    1: {"label": "Rare", "desc": "Could happen in theory"},
}

RISK_TIERS = {
    (15, 25): {"level": "Extreme", "action": "Do not proceed. Must eliminate risk before re-assessment.", "color": "FF0000"},
    (8, 14): {"level": "High", "action": "Requires advanced control measures + project manager approval.", "color": "FF6600"},
    (4, 7): {"level": "Medium", "action": "Requires control measures + attendant monitoring.", "color": "FFFF00"},
    (1, 3): {"level": "Low", "action": "Standard PPE + attendant monitoring.", "color": "00AA00"},
}


def calculate_risk(severity: int, likelihood: int) -> dict:
    """Calculate risk score and tier.

    Args:
        severity: 1-5 (see SEVERITY_LEVELS)
        likelihood: 1-5 (see LIKELIHOOD_LEVELS)

    Returns:
        dict with: score, level, action, color, severity_label,
        likelihood_label, severity_desc, likelihood_desc
    """
    score = severity * likelihood
    tier = get_risk_tier(score)
    sev = SEVERITY_LEVELS.get(severity, {"label": "Unknown", "desc": ""})
    lik = LIKELIHOOD_LEVELS.get(likelihood, {"label": "Unknown", "desc": ""})

    return {
        "score": score,
        "level": tier["level"],
        "action": tier["action"],
        "color": tier["color"],
        "severity_label": sev["label"],
        "severity_desc": sev["desc"],
        "likelihood_label": lik["label"],
        "likelihood_desc": lik["desc"],
    }


def get_risk_tier(score: int) -> dict:
    """Get risk tier from score."""
    for (low, high), tier in RISK_TIERS.items():
        if low <= score <= high:
            return tier.copy()
    return {"level": "Unknown", "action": "Manual review required.", "color": "999999"}


def assess_hazards(hazards: list) -> list:
    """Assess a list of hazard dicts (with severity/likelihood) and add risk info.

    Args:
        hazards: List of hazard dicts from hazard_matcher.identify_hazards()

    Returns:
        Same list with added risk_score, risk_level, risk_action keys
    """
    for hazard in hazards:
        risk = calculate_risk(hazard.get("severity", 3), hazard.get("likelihood", 3))
        hazard["risk_score"] = risk["score"]
        hazard["risk_level"] = risk["level"]
        hazard["risk_action"] = risk["action"]
        hazard["risk_color"] = risk["color"]
        hazard["severity_label"] = risk["severity_label"]
        hazard["likelihood_label"] = risk["likelihood_label"]
    return hazards


def generate_risk_matrix() -> list:
    """Generate a 5x5 risk matrix for visualization.

    Returns:
        List of rows, each row is a list of (score, level, color) tuples.
    Matrix layout: rows = severity (5→1), cols = likelihood (1→5)
    """
    matrix = []
    for sev in range(5, 0, -1):
        row = []
        for lik in range(1, 6):
            risk = calculate_risk(sev, lik)
            row.append({
                "score": risk["score"],
                "level": risk["level"],
                "color": risk["color"],
                "severity": sev,
                "likelihood": lik,
            })
        matrix.append(row)
    return matrix


def get_ventilation_requirement(volume_m3: float) -> dict:
    """Calculate ventilation requirements for a space.

    Args:
        volume_m3: Space volume in cubic meters

    Returns:
        dict with: required_airflow, recommended_equipment, min_ventilation_time
    """
    airflow = volume_m3 * 20  # 20 air changes per hour

    if volume_m3 < 10:
        equipment = "Portable axial fan"
    elif volume_m3 <= 50:
        equipment = "Medium explosion-proof fan"
    else:
        equipment = "Industrial fan + ducting"

    return {
        "space_volume_m3": volume_m3,
        "required_airflow_m3h": round(airflow, 1),
        "air_changes_per_hour": 20,
        "min_ventilation_time_min": 30,
        "recommended_equipment": equipment,
    }
