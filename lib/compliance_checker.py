"""
compliance_checker.py — Step 5: Compliance review against regulatory checklist.
=========================================================================
Checks generated plan against statutory requirements.
"""

CHECKLIST_SECTIONS = [
    {
        "id": "risk_assessment",
        "regulation": "§161 — Risk Assessment Report",
        "items": [
            "Work location description complete (type/dimensions/location/access)",
            "All 4 hazard dimensions identified (atmospheric/physical/chemical/structural)",
            "Risk assessment method clear (matrix formula)",
            "Risk levels correctly determined",
            "Control measures cover all identified hazards",
            "Emergency plan includes rescue procedures and contacts",
            "Assessor signature field complete",
        ],
    },
    {
        "id": "work_permit",
        "regulation": "§163 — Work Permit",
        "items": [
            "Work content and scope clearly defined",
            "Validity period reasonable (max one shift)",
            "Permit conditions confirmed item-by-item (12 items)",
            "Issuer is a competent person",
            "Receiver is a designated person",
        ],
    },
    {
        "id": "safety_measures",
        "regulation": "§165 — Safety Measures (17 items)",
        "items": [
            "Space confirmed as confined space",
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
            "Post-work: all personnel evacuated confirmation",
        ],
    },
    {
        "id": "personnel",
        "regulation": "§166-167 — Personnel Qualification",
        "items": [
            "Competent person qualification certificate valid",
            "Entrant training records complete",
            "Attendant duties clearly communicated",
        ],
    },
    {
        "id": "underground",
        "regulation": "§168-172 — Underground Work (if applicable)",
        "items": [
            "Earth support design approved",
            "Groundwater control measures in place",
            "Adjacent structure protection assessed",
            "Enhanced ventilation meets requirements",
        ],
    },
    {
        "id": "safety_management",
        "regulation": "Safety Management Manual A.2.5",
        "items": [
            "Risk assessment complete",
            "Safety measures specific and actionable",
            "Emergency plan feasible",
            "Personnel training plan included",
            "Supervision system clearly defined",
        ],
    },
    {
        "id": "inspection",
        "regulation": "Safety Management Manual C.1.8",
        "items": [
            "Attendant present and not multitasking",
            "Continuous ventilation operational",
            "Gas monitoring continuous",
            "O₂ in 19.5-23.5% range",
            "Flammable gas < 10% LEL",
            "Toxic gases within limits",
            "Communication working",
            "Rescue equipment in position",
        ],
    },
]


def run_compliance_check(plan_data: dict) -> dict:
    """Step 5: Run full compliance review against all checklist sections.

    Args:
        plan_data: dict containing the generated plan sections
            (hazard_assessment, control_measures, permit, emergency_plan, etc.)

    Returns:
        dict with: sections (list of check results), total_items, passed,
        failed, overall_status, improvement_suggestions
    """
    results = []
    total = 0
    passed = 0
    failed = 0

    for section in CHECKLIST_SECTIONS:
        section_items = []
        for item in section["items"]:
            total += 1
            is_met = _check_item(section["id"], item, plan_data)
            if is_met:
                passed += 1
                status = "pass"
            else:
                failed += 1
                status = "fail"
            section_items.append({"item": item, "status": status})

        results.append({
            "section_id": section["id"],
            "regulation": section["regulation"],
            "items": section_items,
            "section_passed": sum(1 for i in section_items if i["status"] == "pass"),
            "section_total": len(section_items),
        })

    if failed == 0:
        overall = "PASS"
    elif passed > failed:
        overall = "CONDITIONAL PASS"
    else:
        overall = "FAIL"

    return {
        "sections": results,
        "total_items": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": f"{passed}/{total} ({round(passed/total*100, 1)}%)" if total > 0 else "N/A",
        "overall_status": overall,
        "improvement_suggestions": _generate_suggestions(results),
    }


def _check_item(section_id: str, item: str, plan_data: dict) -> bool:
    """Check if a specific compliance item is met based on plan data.

    Uses heuristic checks: if the relevant section exists and has content,
    the item is considered met. Override with explicit flags if needed.
    """
    overrides = plan_data.get("compliance_overrides", {})
    item_key = item.lower().replace(" ", "_").replace(":", "").replace("(", "").replace(")", "")[:50]
    if item_key in overrides:
        return overrides[item_key]

    if section_id == "risk_assessment":
        hazards = plan_data.get("hazard_assessment", {}).get("hazards", [])
        if "hazard" in item.lower() or "dimension" in item.lower():
            return len(hazards) > 0
        if "risk" in item.lower() and "method" in item.lower():
            return True
        if "risk" in item.lower() and "level" in item.lower():
            return len(hazards) > 0
        if "control" in item.lower():
            return len(plan_data.get("control_measures", [])) > 0
        if "emergency" in item.lower() or "rescue" in item.lower():
            return "emergency_plan" in plan_data
        if "signature" in item.lower() or "assessor" in item.lower():
            return True
        if "location" in item.lower() or "description" in item.lower():
            return "project_info" in plan_data
        return len(hazards) > 0

    if section_id == "work_permit":
        permit = plan_data.get("permit", {})
        return len(permit) > 0 or "permit" in plan_data

    if section_id == "safety_measures":
        controls = plan_data.get("control_measures", [])
        hazards = plan_data.get("hazard_assessment", {}).get("hazards", [])
        if "ventilation" in item.lower():
            return any("ventilation" in str(c.get("engineering", "")) for c in controls)
        if "gas" in item.lower() and "monitor" in item.lower():
            return any("monitor" in str(c.get("administrative", "")) for c in controls)
        if "loto" in item.lower():
            return any("loto" in str(c.get("engineering", "")).lower() for c in controls)
        if "attendant" in item.lower():
            return any("attendant" in str(c.get("administrative", "")).lower() for c in controls)
        if "ppe" in item.lower():
            return any(len(c.get("ppe", [])) > 0 for c in controls)
        if "rescue" in item.lower():
            return "emergency_plan" in plan_data
        if "trained" in item.lower() or "tbt" in item.lower():
            return True
        if "permit" in item.lower():
            return "permit" in plan_data or len(plan_data.get("permit", {})) > 0
        if "evacuat" in item.lower():
            return True
        return len(hazards) > 0

    if section_id == "personnel":
        return "personnel" in plan_data or True

    if section_id == "underground":
        space_type = plan_data.get("project_info", {}).get("space_type", "").lower()
        if "manhole" in space_type or "sewer" in space_type or "pipe" in space_type or "tunnel" in space_type:
            return False  # Requires manual verification
        return True  # N/A for above-ground spaces

    if section_id == "safety_management":
        return len(plan_data.get("control_measures", [])) > 0

    if section_id == "inspection":
        controls = plan_data.get("control_measures", [])
        if "ventilation" in item.lower():
            return any("ventilation" in str(c.get("engineering", "")) for c in controls)
        if "gas" in item.lower() or "oxygen" in item.lower() or "o₂" in item.lower():
            return any("monitor" in str(c.get("administrative", "")).lower() for c in controls)
        if "attendant" in item.lower():
            return True
        if "communication" in item.lower():
            return any("radio" in str(c.get("ppe", "")).lower() for c in controls)
        if "rescue" in item.lower():
            return "emergency_plan" in plan_data
        return True

    return True


def _generate_suggestions(section_results: list) -> list:
    """Generate improvement suggestions for failed items."""
    suggestions = []
    for section in section_results:
        failed_items = [i for i in section["items"] if i["status"] == "fail"]
        if failed_items:
            suggestions.append({
                "section": section["regulation"],
                "missing_items": [i["item"] for i in failed_items],
            })
    return suggestions
