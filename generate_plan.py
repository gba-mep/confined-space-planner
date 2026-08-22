#!/usr/bin/env python3
"""
generate_plan.py — Main CLI entry point.
=========================================================================
Confined Space Construction Plan Generator

5-step pipeline:
  1. Situation Analysis      — match space type to hazard profile
  2. Hazard Identification   — expand to full hazard details
  3. Control Measures        — generate engineering/administrative/PPE
  4. Document Writing        — assemble complete Word document
  5. Compliance Review       — check against regulatory checklist

Usage:
  python generate_plan.py --input examples/manhole_input.json --output plan.docx
  python generate_plan.py --input examples/water_tank_input.json --output water_tank_plan.docx
"""

import argparse
import json
import sys
from pathlib import Path

from lib.hazard_matcher import analyze_situation, identify_hazards, get_gas_standards, get_legal_definition
from lib.risk_calculator import assess_hazards, get_ventilation_requirement, generate_risk_matrix
from lib.control_generator import generate_controls, get_permit_conditions, get_safety_measures
from lib.compliance_checker import run_compliance_check
from lib.doc_builder import generate_plan_docx


def parse_space_dimensions(dim_str: str) -> float:
    """Parse dimension string like '3m x 3m x 3m' to volume in m³."""
    try:
        parts = dim_str.lower().replace("m", "").replace("×", "x").split("x")
        dims = [float(p.strip()) for p in parts if p.strip()]
        if len(dims) >= 3:
            return dims[0] * dims[1] * dims[2]
        elif len(dims) == 2:
            return dims[0] * dims[1] * 2.5  # assume 2.5m height
        return 10.0  # default
    except Exception:
        return 10.0


def run_pipeline(input_data: dict) -> dict:
    """Run the full 5-step pipeline.

    Args:
        input_data: dict with project_info, space_description, work_content, special_requirements

    Returns:
        Complete plan data dict ready for doc_builder
    """
    space = input_data.get("space_description", {})
    special = input_data.get("special_requirements", {})
    space_type = space.get("type", "unknown")
    known_hazards = special.get("known_hazards", [])
    if known_hazards:
        known_hazards = [h.strip() for h in known_hazards.split(",")] if isinstance(known_hazards, str) else known_hazards

    # --- Step 1: Situation Analysis ---
    print("[1/5] Situation analysis...")
    situation = analyze_situation(space_type, known_hazards)
    print(f"      Space type: {space_type}")
    print(f"      Confirmed confined: {situation['is_confirmed_confined']}")
    print(f"      Primary hazards: {situation['primary_hazards']}")
    print(f"      Secondary hazards: {situation['secondary_hazards']}")

    # --- Step 2: Hazard Identification + Risk Assessment ---
    print("[2/5] Hazard identification + risk assessment...")
    hazards = identify_hazards(situation["all_hazards"])
    hazards = assess_hazards(hazards)
    for h in hazards:
        print(f"      {h['name']}: severity={h['severity']}, likelihood={h['likelihood']}, "
              f"score={h['risk_score']}, level={h['risk_level']}")

    # Ventilation calculation
    dims = space.get("dimensions", "3m x 3m x 3m")
    volume = parse_space_dimensions(dims)
    vent_req = get_ventilation_requirement(volume)
    print(f"      Ventilation: {vent_req['required_airflow_m3h']} m³/h, {vent_req['recommended_equipment']}")

    # Gas standards
    gas_std = get_gas_standards()
    legal_def = get_legal_definition()

    # --- Step 3: Control Measures ---
    print("[3/5] Generating control measures...")
    controls = generate_controls(situation["all_hazards"])
    total_measures = sum(len(c.get("engineering", [])) + len(c.get("administrative", [])) + len(c.get("ppe", [])) for c in controls)
    print(f"      Generated {total_measures} control measures across {len(controls)} hazards")

    # --- Step 4: Document Writing ---
    print("[4/5] Assembling plan data...")
    plan_data = {
        "project_info": input_data.get("project_info", {}),
        "space_description": space,
        "work_content": input_data.get("work_content", {}),
        "hazard_assessment": {
            "hazards": hazards,
            "legal_definition": legal_def,
            "gas_standards": gas_std,
            "ventilation_requirement": vent_req,
            "situation": situation,
        },
        "control_measures": controls,
        "permit": {
            "conditions": get_permit_conditions(),
            "safety_measures": get_safety_measures(),
        },
    }

    # --- Step 5: Compliance Review ---
    print("[5/5] Compliance review...")
    compliance = run_compliance_check(plan_data)
    plan_data["compliance_report"] = compliance
    print(f"      Total: {compliance['total_items']} | Passed: {compliance['passed']} | "
          f"Failed: {compliance['failed']} | Rate: {compliance['pass_rate']}")
    print(f"      Overall: {compliance['overall_status']}")

    return plan_data


def main():
    parser = argparse.ArgumentParser(
        description="Confined Space Construction Plan Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_plan.py --input examples/manhole_input.json --output plan.docx
  python generate_plan.py --input examples/water_tank_input.json --output water_tank.docx
  python generate_plan.py --input custom.json --output custom_plan.docx --json

The --json flag also exports the plan data as JSON for integration.
        """,
    )
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON file")
    parser.add_argument("--output", "-o", default="confined_space_plan.docx", help="Output .docx path (default: confined_space_plan.docx)")
    parser.add_argument("--json", action="store_true", help="Also export plan data as JSON")
    parser.add_argument("--matrix", action="store_true", help="Print risk matrix to console")
    args = parser.parse_args()

    # Load input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    print(f"{'='*60}")
    print(f"  Confined Space Construction Plan Generator")
    print(f"  Input:  {input_path.name}")
    print(f"  Output: {args.output}")
    print(f"{'='*60}\n")

    # Run pipeline
    plan_data = run_pipeline(input_data)

    # Print risk matrix if requested
    if args.matrix:
        print("\n" + "="*60)
        print("  Risk Matrix (Severity × Likelihood)")
        print("="*60)
        matrix = generate_risk_matrix()
        print(f"\n  {'':12s}", end="")
        for lik_label in ["1 (Rare)", "2 (Unlik)", "3 (Poss)", "4 (Likely)", "5 (Certain)"]:
            print(f" {lik_label:>12s}", end="")
        print()
        for row in matrix:
            sev = row[0]["severity"]
            sev_labels = {5: "5 (Catast)", 4: "4 (Severe)", 3: "3 (Moder)", 2: "2 (Minor)", 1: "1 (Neglig)"}
            print(f"  {sev_labels.get(sev, str(sev)):12s}", end="")
            for cell in row:
                print(f"  {cell['score']:2d} {cell['level'][:4]:>4s}", end="")
            print()

    # Generate Word document
    print(f"\n{'='*60}")
    print(f"  Generating Word document: {args.output}")
    print(f"{'='*60}")
    output_path = generate_plan_docx(plan_data, args.output)
    print(f"  ✓ Saved: {output_path}")

    # Export JSON if requested
    if args.json:
        json_path = args.output.replace(".docx", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ JSON exported: {json_path}")

    print(f"\n{'='*60}")
    print(f"  Done! {compliance_count(plan_data)} compliance items checked.")
    print(f"{'='*60}")


def compliance_count(plan_data):
    """Get compliance summary string."""
    c = plan_data.get("compliance_report", {})
    return f"{c.get('passed', 0)}/{c.get('total_items', 0)} passed ({c.get('overall_status', 'N/A')})"


if __name__ == "__main__":
    main()
