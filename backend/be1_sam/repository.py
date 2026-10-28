"""Sam: read the provided CSVs without changing the source data."""
import csv
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from shared.contracts import Catalog, Location, ReferenceOption, WeatherHour, Profile
from .health_catalog import INFECTIOUS, ALLERGIES

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("WEATHERWISE_DATA_DIR", str(ROOT / "data" / "synthetic")))

class DatasetRepository:
    def __init__(self, directory: Path = DATA):
        def read(name):
            with (directory / name).open(encoding="utf-8-sig", newline="") as stream:
                return list(csv.DictReader(stream))
        self.locations = {r["location_id"]: r for r in read("01_locations.csv")}
        self.conditions = {r["condition_id"]: r for r in read("04_medical_conditions_reference.csv")}
        self.occupations = {r["occupation_id"]: r for r in read("05_occupations_exposure_reference.csv")}
        self.weather = read("02_weather_hourly_observed.csv")
        self.dates = sorted({r["timestamp"][:10] for r in self.weather})

    def catalog(self) -> Catalog:
        return Catalog(
            locations=[Location(**r) for r in self.locations.values()],
            conditions=[ReferenceOption(id=k, name=r["condition_name"], group="allergy" if k == "C10" else "other" if k in {"C08", "C15"} else "noncommunicable") for k, r in self.conditions.items()],
            occupations=[ReferenceOption(id=k, name=r["occupation"]) for k, r in self.occupations.items()],
            dates=self.dates,
            infectious_conditions=[ReferenceOption(id=k, name=v, group="communicable") for k, v in INFECTIOUS.items()],
            allergies=[ReferenceOption(id=k, name=v, group="food" if k not in {"pollen", "dust", "mould", "pets"} else "environmental") for k, v in ALLERGIES.items()],
        )

    def validate_profile(self, profile: Profile):
        if profile.home_location_id not in self.locations:
            raise ValueError("Unknown location")
        if profile.occupation_id not in self.occupations:
            raise ValueError("Unknown occupation")
        if any(c not in self.conditions for c in profile.condition_ids):
            raise ValueError("Unknown condition")
        if any(c not in INFECTIOUS for c in profile.infectious_condition_ids) or any(a not in ALLERGIES for a in profile.allergy_ids):
            raise ValueError("Unknown disease or allergy selection")

    def day(self, location_id: str, date: str) -> list[WeatherHour]:
        if location_id not in self.locations or date not in self.dates:
            raise ValueError("Location or date is not present in the synthetic dataset")
        rows = [r for r in self.weather if r["location_id"] == location_id and r["timestamp"].startswith(date)]
        return [WeatherHour(
            timestamp=datetime.fromisoformat(r["timestamp"]).replace(tzinfo=ZoneInfo("Asia/Kolkata")).isoformat(),
            **{k: r[k] for k in WeatherHour.model_fields if k != "timestamp" and k in r},
        ) for r in sorted(rows, key=lambda r: r["timestamp"])]
