"""Sam: regenerate agreed contracts and Shreshta's fixed mock fixtures.

Run from repository root: python scripts/export_contracts.py [--check]
"""
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.be1_sam.app import create_app
from backend.be1_sam.repository import DatasetRepository
from backend.be2_metta.service import build_dashboard
from shared.contracts import Profile, Location

def exports():
    repo = DatasetRepository()
    profile = Profile()
    dashboard = build_dashboard(profile, Location(**repo.locations[profile.home_location_id]), repo.day(profile.home_location_id, "2026-05-08"), repo.conditions, repo.occupations[profile.occupation_id], "2026-05-08")
    return {
        "shared/openapi.json": create_app().openapi(),
        "shared/dashboard.schema.json": type(dashboard).model_json_schema(),
        "frontend_shreshta/mock/dashboard.json": dashboard.model_dump(),
        "frontend_shreshta/mock/catalog.json": repo.catalog().model_dump(),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    different = []
    for name, payload in exports().items():
        path = ROOT / name
        content = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content: different.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding="utf-8")
            print(f"Wrote {name}")
    if different:
        raise SystemExit("Contract/fixture drift: " + ", ".join(different))
    if args.check: print("Contracts and frontend fixtures match the backend.")
