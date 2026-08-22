"""
control_generator.py — Step 3: Generate control measures by hierarchy.
=========================================================================
Elimination → Substitution → Engineering → Administrative → PPE
"""

CONTROL_HIERARCHY = [
    "elimination",
    "substitution",
    "engineering",
    "administrative",
    "ppe",
]

HAZARD_CONTROLS = {
    "oxygen_deficiency": {
        "engineering": [
            "Mechanical ventilation ≥ 30 min before entry",
            "Continuous ventilation during occupancy",
            "Calculated airflow: volume × 20 air changes/hour",
        ],
        "administrative": [
            "Continuous gas monitoring (O₂ alarm at <20% or >23%)",
            "Attendant stationed outside at all times",
            "Entry permit valid for one shift only",
        ],
        "ppe": [
            "SCBA (Self-Contained Breathing Apparatus) if O₂ < 19.5%",
        ],
    },
    "H2S": {
        "engineering": [
            "Ventilation ≥ 30 min before entry",
            "Isolate sewage sources (LOTO on valves)",
        ],
        "administrative": [
            "Gas monitoring: H₂S alarm at >5 ppm, evacuate at >10 ppm",
            "No solo entry — attendant required",
            "Emergency rescue plan with SCBA rescue team",
        ],
        "ppe": [
            "SCBA if H₂S > 10 ppm",
            "Gas detector with H₂S sensor on each entrant",
        ],
    },
    "CO": {
        "engineering": [
            "Eliminate combustion sources near entry (relocate generators)",
            "Ventilation ≥ 30 min before entry",
        ],
        "administrative": [
            "Gas monitoring: CO alarm at >15 ppm, evacuate at >25 ppm",
            "Attendant stationed outside",
        ],
        "ppe": [
            "SCBA if CO > 25 ppm",
            "Gas detector with CO sensor",
        ],
    },
    "flammable_gas": {
        "engineering": [
            "Ventilation with explosion-proof fan",
            "Purge space with inert gas if LEL > 10%",
            "Eliminate ignition sources (explosion-proof tools only)",
        ],
        "administrative": [
            "Gas monitoring: LEL alarm at >5%, evacuate at >10%",
            "Hot work permit required if welding/cutting",
            "Fire watch stationed outside",
        ],
        "ppe": [
            "Explosion-proof equipment only",
            "Anti-static clothing",
            "Gas detector with LEL sensor",
        ],
    },
    "VOC": {
        "engineering": [
            "Ventilation ≥ 30 min before entry",
            "Remove chemical containers from space",
            "Steam clean or water flush residue",
        ],
        "administrative": [
            "Gas monitoring: VOC meter calibrated to target substance",
            "MSDS (Safety Data Sheet) available on-site",
            "Entry permit with chemical exposure assessment",
        ],
        "ppe": [
            "Chemical-resistant gloves + goggles",
            "Respirator with organic vapor cartridge (if O₂ normal)",
            "SCBA if O₂ < 19.5% or VOC concentration unknown",
        ],
    },
    "electrocution": {
        "engineering": [
            "LOTO (Lockout/Tagout) on all electrical circuits",
            "Use 12V/24V safety lighting inside space",
            "RCD/GFCI on all power tools",
        ],
        "administrative": [
            "Verify zero energy state before entry",
            "Competent person confirms LOTO effectiveness",
        ],
        "ppe": [
            "Insulated rubber gloves",
            "Dielectric safety boots",
            "Insulated tools",
        ],
    },
    "fall": {
        "engineering": [
            "Install tripod + davit at entry point",
            "Guardrail around opening",
            "Secure ladder inside space",
        ],
        "administrative": [
            "Fall protection plan for entries > 2m depth",
            "Attendant monitors entrant's harness line",
        ],
        "ppe": [
            "Full-body harness",
            "Lifeline (rope) connected to tripod",
            "Safety helmet with chin strap",
        ],
    },
    "drowning": {
        "engineering": [
            "Isolate water sources (LOTO on valves, blank off pipes)",
            "Dewatering pump on standby",
            "Float switch alarm for water level",
        ],
        "administrative": [
            "Attendant monitors for water ingress",
            "Emergency evacuation at first sign of rising water",
        ],
        "ppe": [
            "Life jacket",
            "Full-body harness + lifeline for extraction",
        ],
    },
    "engulfment": {
        "engineering": [
            "Shoring/bracing for unstable material",
            "Isolate material feed sources",
        ],
        "administrative": [
            "No entry if material instability detected",
            "Continuous monitoring of surrounding stability",
        ],
        "ppe": [
            "Full-body harness + lifeline",
            "Safety helmet",
        ],
    },
    "collapse": {
        "engineering": [
            "Install shoring (timber/hydraulic) for excavation > 1.2m",
            "Inspect support structures before entry",
            "Remove surcharge loads near excavation edge",
        ],
        "administrative": [
            "Daily inspection by competent person",
            "Stop work if ground movement detected",
        ],
        "ppe": [
            "Safety helmet",
            "Steel-toe boots",
        ],
    },
    "physical_entrapment": {
        "engineering": [
            "Widen access if feasible",
            "Remove internal obstructions before entry",
        ],
        "administrative": [
            "Two-person communication (lifeline + voice contact)",
            "Attendant monitors entrant position",
        ],
        "ppe": [
            "Full-body harness + lifeline",
        ],
    },
    "mechanical_crush": {
        "engineering": [
            "LOTO on all mechanical equipment (mixers, fans)",
            "Guard moving parts",
        ],
        "administrative": [
            "Verify zero mechanical energy before entry",
            "Attendant confirms LOTO integrity",
        ],
        "ppe": [
            "Safety helmet",
            "Steel-toe boots",
        ],
    },
    "heat_stress": {
        "engineering": [
            "Mechanical ventilation to reduce ambient temperature",
            "Schedule work for cooler hours (early morning/evening)",
            "Heat shielding if radiation source present",
        ],
        "administrative": [
            "Work/rest cycle: 45 min work / 15 min rest (at 32-35°C WBGT)",
            "Acclimatization period for new workers (7 days)",
            "Monitor workers for heat illness symptoms",
        ],
        "ppe": [
            "Cooling vest",
            "Light-colored, breathable clothing",
            "Plenty of drinking water available",
        ],
    },
    "noise": {
        "engineering": [
            "Use low-noise equipment where possible",
            "Sound-absorbing baffles at fan intake/exhaust",
        ],
        "administrative": [
            "Limit exposure time: 85 dB(A) = 8h, 88 dB(A) = 4h",
            "Rotate workers to reduce individual exposure",
        ],
        "ppe": [
            "Ear muffs or ear plugs (NRR ≥ 25 dB)",
        ],
    },
    "chemical_burn": {
        "engineering": [
            "Drain and flush chemical residue with water",
            "Neutralize acid/alkali with appropriate agent",
            "Ventilation to remove vapors",
        ],
        "administrative": [
            "SDS available for all chemicals present",
            "Emergency eyewash and shower within 10 seconds travel",
            "Entry permit includes chemical inventory",
        ],
        "ppe": [
            "Chemical-resistant suit (Tyvek or equivalent)",
            "Chemical-resistant gloves + boots",
            "Full-face shield + goggles",
        ],
    },
    "dust_explosion": {
        "engineering": [
            "Ventilation to reduce dust concentration below LEL",
            "Eliminate ignition sources (explosion-proof equipment)",
            "Bonding and grounding of all equipment",
        ],
        "administrative": [
            "Dust monitoring: evacuate at > 25% of MEC",
            "Hot work permit required for any ignition source",
            "Fire watch with extinguisher rated for Class D",
        ],
        "ppe": [
            "Anti-static clothing",
            "Respirator with P100 particulate filter",
        ],
    },
    "biological": {
        "engineering": [
            "Disinfect space with appropriate biocide",
            "Ventilation to reduce airborne pathogens",
            "Remove animal waste/nesting material",
        ],
        "administrative": [
            "Tetanus vaccination current for all entrants",
            "Biological hazard assessment completed",
            "Post-exposure medical monitoring plan",
        ],
        "ppe": [
            "PPE suit (disposable or washable)",
            "Nitrile gloves (double-gloved)",
            "Half-face respirator with P100 filter",
            "Safety goggles or face shield",
        ],
    },
    "poor_ventilation": {
        "engineering": [
            "Mechanical ventilation with supply + exhaust",
            "Calculated airflow: volume × 20 air changes/hour",
            "Air quality monitoring at 3 depths (top/middle/bottom)",
        ],
        "administrative": [
            "Ventilation runs continuously during occupancy",
            "Gas monitoring every 30 minutes minimum",
        ],
        "ppe": [
            "Gas detector (4-gas: O₂, CO, H₂S, LEL) on each entrant",
        ],
    },
    "dust": {
        "engineering": [
            "Wet cutting methods to suppress dust",
            "Local exhaust ventilation at dust source",
        ],
        "administrative": [
            "Respirable dust monitoring",
            "Limit exposure time per shift",
        ],
        "ppe": [
            "Half-face respirator with P100 filter",
            "Safety goggles",
        ],
    },
}

PERMIT_12_CONDITIONS = [
    "Risk assessment completed",
    "LOTO executed (if applicable)",
    "Ventilation ≥ 30 min and gas readings safe",
    "All entrants received TBT (Toolbox Talk)",
    "Attendant is in position",
    "Communication equipment tested and working",
    "PPE inspected and donned",
    "Rescue equipment in position",
    "Explosion-proof lighting in position (if applicable)",
    "Entry/exit log prepared",
    "Emergency plan communicated to all personnel",
    "Work scope confirmed — no scope creep",
]

SAFETY_17_MEASURES = [
    "Confirm space is a confined space",
    "Risk assessment completed",
    "Work permit issued",
    "Competent person designated",
    "Workers trained (TBT received)",
    "Pre-entry ventilation ≥ 30 min",
    "Continuous gas monitoring established",
    "Ventilation equipment running continuously",
    "LOTO executed (if applicable)",
    "Attendant stationed outside",
    "Communication equipment in position",
    "Emergency rescue equipment in position",
    "Rescue personnel on standby",
    "PPE equipped and inspected",
    "Entry/exit registration system established",
    "Explosion-proof lighting in position (if applicable)",
    "Post-work: confirm all personnel evacuated",
]

RESCUE_EQUIPMENT = [
    {"item": "Tripod", "quantity": "1 set", "purpose": "Personnel raising/lowering"},
    {"item": "Winch/Davit", "quantity": "1 set", "purpose": "配合 tripod"},
    {"item": "Rescue rope", "quantity": "2", "purpose": "Connect to harness"},
    {"item": "Full-body harness", "quantity": "Per person", "purpose": "Each entrant"},
    {"item": "SCBA", "quantity": "2 sets", "purpose": "Rescue personnel use"},
    {"item": "First aid kit", "quantity": "1 set", "purpose": "Basic first aid"},
    {"item": "CPR mask", "quantity": "1", "purpose": "Artificial respiration"},
    {"item": "Explosion-proof radio", "quantity": "2", "purpose": "Internal/external communication"},
    {"item": "Explosion-proof light", "quantity": "2", "purpose": "Emergency lighting"},
]


def generate_controls(hazard_keys: list) -> list:
    """Step 3: Generate control measures for each hazard.

    Args:
        hazard_keys: List of hazard keys from hazard_matcher

    Returns:
        List of dicts with: hazard_key, engineering, administrative, ppe
    """
    results = []
    for key in hazard_keys:
        controls = HAZARD_CONTROLS.get(key, {
            "engineering": ["Assess and mitigate per site conditions"],
            "administrative": ["Competent person to determine specific controls"],
            "ppe": ["Site-specific PPE assessment required"],
        })
        results.append({
            "hazard_key": key,
            "engineering": controls.get("engineering", []),
            "administrative": controls.get("administrative", []),
            "ppe": controls.get("ppe", []),
        })
    return results


def get_permit_conditions() -> list:
    """Return the 12 standard permit conditions checklist."""
    return PERMIT_12_CONDITIONS.copy()


def get_safety_measures() -> list:
    """Return the 17 statutory safety measures."""
    return SAFETY_17_MEASURES.copy()


def get_rescue_equipment() -> list:
    """Return rescue equipment checklist."""
    return [item.copy() for item in RESCUE_EQUIPMENT]


def get_personnel_requirements() -> list:
    """Return required personnel roles."""
    return [
        {"role": "Competent Person", "requirement": "Holds safety qualification certificate, responsible for assessment & approval", "quantity": "1"},
        {"role": "Authorized Entrant", "requirement": "Trained, holds valid permit", "quantity": "As needed"},
        {"role": "Attendant (Standby)", "requirement": "Must not multi-task, must be present at all times", "quantity": "1"},
        {"role": "Rescue Personnel", "requirement": "Trained, equipped with rescue gear on standby", "quantity": "1-2"},
    ]
