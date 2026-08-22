"""
hazard_matcher.py — Step 1-2: Situation analysis + hazard identification.
=========================================================================
Matches input space type against hazard library, returns identified hazards.
"""

SPACE_TYPE_HAZARDS = {
    "manhole": {
        "primary": ["H2S", "oxygen_deficiency", "drowning"],
        "secondary": ["CO", "fall", "engulfment"],
    },
    "sewer": {
        "primary": ["H2S", "oxygen_deficiency", "drowning"],
        "secondary": ["CO", "fall", "engulfment", "biological"],
    },
    "water_tank": {
        "primary": ["oxygen_deficiency", "electrocution", "fall"],
        "secondary": ["biological", "drowning"],
    },
    "pipe": {
        "primary": ["oxygen_deficiency", "flammable_gas", "physical_entrapment"],
        "secondary": ["noise", "heat_stress"],
    },
    "duct": {
        "primary": ["oxygen_deficiency", "physical_entrapment"],
        "secondary": ["noise", "heat_stress"],
    },
    "storage_tank": {
        "primary": ["VOC", "oxygen_deficiency", "chemical_burn"],
        "secondary": ["dust_explosion", "drowning"],
    },
    "boiler": {
        "primary": ["heat_stress", "oxygen_deficiency"],
        "secondary": ["electrocution", "mechanical_crush"],
    },
    "tunnel": {
        "primary": ["oxygen_deficiency", "collapse", "drowning"],
        "secondary": ["noise", "dust", "poor_ventilation"],
    },
    "basement": {
        "primary": ["oxygen_deficiency", "collapse"],
        "secondary": ["drowning", "electrocution"],
    },
}

HAZARD_DETAILS = {
    "oxygen_deficiency": {
        "name": "Oxygen Deficiency (O₂ < 19.5%)",
        "category": "atmospheric",
        "source": "Biological respiration, oxidation reactions",
        "scenarios": "Long-sealed spaces, decaying organic matter consuming oxygen",
        "severity": 5,
        "likelihood": 4,
    },
    "H2S": {
        "name": "Hydrogen Sulfide (H₂S > 10 ppm)",
        "category": "atmospheric",
        "source": "Sulfate-reducing bacteria, sewage decomposition",
        "scenarios": "Sewers, sewage treatment tanks, manholes",
        "severity": 5,
        "likelihood": 4,
    },
    "CO": {
        "name": "Carbon Monoxide (CO > 25 ppm)",
        "category": "atmospheric",
        "source": "Incomplete combustion, engine exhaust",
        "scenarios": "Generator proximity, welding fumes",
        "severity": 5,
        "likelihood": 3,
    },
    "flammable_gas": {
        "name": "Flammable Gas (> 10% LEL)",
        "category": "atmospheric",
        "source": "Organic decomposition, fuel leakage",
        "scenarios": "Sewer pipes, chemical storage tanks",
        "severity": 5,
        "likelihood": 3,
    },
    "VOC": {
        "name": "Volatile Organic Compounds",
        "category": "atmospheric",
        "source": "Cleaning agents, solvents, coatings",
        "scenarios": "Using thinner or diluent inside tanks",
        "severity": 4,
        "likelihood": 3,
    },
    "electrocution": {
        "name": "Electrocution",
        "category": "physical",
        "source": "Damp environment + electrical tools",
        "scenarios": "Using electrical equipment inside water tanks/pipes",
        "severity": 5,
        "likelihood": 3,
    },
    "fall": {
        "name": "Fall from Height (> 2m)",
        "category": "physical",
        "source": "Deep shafts without fall protection",
        "scenarios": "Manholes, vertical pipe shafts",
        "severity": 4,
        "likelihood": 3,
    },
    "drowning": {
        "name": "Drowning",
        "category": "physical",
        "source": "Water ingress, liquid accumulation",
        "scenarios": "Tank cleaning, drainage pipe work",
        "severity": 5,
        "likelihood": 3,
    },
    "engulfment": {
        "name": "Engulfment / Burial",
        "category": "physical",
        "source": "Material collapse, unstable surroundings",
        "scenarios": "Unbraced soil, underground pipe work",
        "severity": 5,
        "likelihood": 2,
    },
    "collapse": {
        "name": "Structural Collapse",
        "category": "structural",
        "source": "Unsupported earth/structure",
        "scenarios": "Underground pipes, excavation bases",
        "severity": 5,
        "likelihood": 2,
    },
    "physical_entrapment": {
        "name": "Physical Entrapment",
        "category": "physical",
        "source": "Narrow/complex internal structure",
        "scenarios": "Pipes with baffles, branch junctions",
        "severity": 4,
        "likelihood": 2,
    },
    "mechanical_crush": {
        "name": "Mechanical Crush Injury",
        "category": "physical",
        "source": "Narrow space + rotating equipment",
        "scenarios": "Mixers, fans inside boilers/tanks",
        "severity": 4,
        "likelihood": 2,
    },
    "heat_stress": {
        "name": "Heat Stress",
        "category": "physical",
        "source": "Sealed + no ventilation + summer heat",
        "scenarios": "Rooftop water tanks, boilers",
        "severity": 3,
        "likelihood": 4,
    },
    "noise": {
        "name": "Noise (Echo + Equipment)",
        "category": "physical",
        "source": "Echo + fans/pumps in narrow space",
        "scenarios": "Using pneumatic tools in small spaces",
        "severity": 2,
        "likelihood": 4,
    },
    "chemical_burn": {
        "name": "Chemical Burn",
        "category": "chemical",
        "source": "Strong acid/alkali residue",
        "scenarios": "Chemical storage tank cleaning",
        "severity": 4,
        "likelihood": 3,
    },
    "dust_explosion": {
        "name": "Dust Explosion",
        "category": "chemical",
        "source": "Combustible dust concentration",
        "scenarios": "Grain silos, powder transport pipes",
        "severity": 5,
        "likelihood": 1,
    },
    "biological": {
        "name": "Biological Hazard",
        "category": "biological",
        "source": "Sewage, mold, animal waste",
        "scenarios": "Sewers, abandoned tanks",
        "severity": 3,
        "likelihood": 3,
    },
    "poor_ventilation": {
        "name": "Poor Ventilation",
        "category": "atmospheric",
        "source": "Inadequate air exchange",
        "scenarios": "Long tunnels, deep basements",
        "severity": 3,
        "likelihood": 4,
    },
    "dust": {
        "name": "Dust Hazard",
        "category": "physical",
        "source": "Construction dust in sealed space",
        "scenarios": "Tunneling, concrete cutting",
        "severity": 2,
        "likelihood": 4,
    },
}

GAS_STANDARDS = {
    "O2": {"safe_range": "19.5% - 23.5%", "danger_low": 19.5, "danger_high": 23.5, "unit": "%"},
    "CO": {"safe_range": "≤ 25 ppm", "danger_threshold": 25, "unit": "ppm"},
    "H2S": {"safe_range": "≤ 10 ppm", "danger_threshold": 10, "unit": "ppm"},
    "LEL": {"safe_range": "≤ 10%", "danger_threshold": 10, "unit": "%"},
    "VOC": {"safe_range": "Substance-specific", "danger_threshold": None, "unit": "varies"},
}

LEGAL_DEFINITION_6_DANGERS = [
    "Explosion (flammable gas/dust exceeds safe limits)",
    "Oxygen deficiency (O₂ < 19.5%)",
    "Poisoning (toxic gas exceeds exposure limits)",
    "Drowning (liquid ingress/accumulation)",
    "High temperature (extreme environmental heat)",
    "High pressure (residual pressure in pipes/containers)",
]


def analyze_situation(space_type: str, known_hazards: list = None) -> dict:
    """Step 1: Situation analysis — determine if space is legally confined,
    match space type to hazard profile.

    Args:
        space_type: One of SPACE_TYPE_HAZARDS keys (manhole, water_tank, etc.)
        known_hazards: Optional list of user-specified known hazard keys

    Returns:
        dict with keys: space_type, is_confirmed_confined, legal_definition,
                        primary_hazards, secondary_hazards, all_hazards
    """
    space_type_lower = space_type.lower().replace(" ", "_").replace("-", "_")

    if space_type_lower not in SPACE_TYPE_HAZARDS:
        known_hazards = known_hazards or []
        return {
            "space_type": space_type,
            "is_confirmed_confined": True,
            "legal_definition": "Space presents one or more of 6 statutory dangers",
            "primary_hazards": [],
            "secondary_hazards": [],
            "all_hazards": known_hazards,
            "warning": f"Space type '{space_type}' not in preset library; hazards based on user input only.",
        }

    hazard_profile = SPACE_TYPE_HAZARDS[space_type_lower]
    primary = hazard_profile["primary"]
    secondary = hazard_profile["secondary"]

    if known_hazards:
        for h in known_hazards:
            if h not in primary and h not in secondary:
                primary.append(h)

    all_hazards = primary + secondary

    return {
        "space_type": space_type,
        "is_confirmed_confined": True,
        "legal_definition": "Space presents one or more of 6 statutory dangers",
        "primary_hazards": primary,
        "secondary_hazards": secondary,
        "all_hazards": all_hazards,
    }


def identify_hazards(hazard_keys: list) -> list:
    """Step 2: Hazard identification — expand hazard keys to full details.

    Args:
        hazard_keys: List of hazard keys from analyze_situation()

    Returns:
        List of hazard detail dicts with name, category, source, scenarios,
        severity, likelihood
    """
    results = []
    for key in hazard_keys:
        if key in HAZARD_DETAILS:
            detail = HAZARD_DETAILS[key].copy()
            detail["key"] = key
            results.append(detail)
        else:
            results.append({
                "key": key,
                "name": key,
                "category": "unknown",
                "source": "User-specified",
                "scenarios": "Not in preset library",
                "severity": 3,
                "likelihood": 3,
            })
    return results


def get_gas_standards() -> dict:
    """Return gas monitoring standards for ventilation and testing."""
    return GAS_STANDARDS.copy()


def get_legal_definition() -> list:
    """Return the 6 statutory dangers defining confined spaces."""
    return LEGAL_DEFINITION_6_DANGERS.copy()
