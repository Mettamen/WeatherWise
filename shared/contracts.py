"""Shared v1 contract. Owner: Sam; changes require Metta + Shreshta review."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class Profile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    display_name: str = Field(default="Alex", min_length=1, max_length=40)
    age: int = Field(default=35, ge=18, le=100)
    home_location_id: str = "LOC01"
    occupation_id: str = "O08"
    condition_ids: list[str] = Field(default_factory=list, max_length=15)
    infectious_condition_ids: list[str] = Field(default_factory=list, max_length=20)
    allergy_ids: list[str] = Field(default_factory=list, max_length=25)
    other_allergy: str = Field(default="", max_length=120)
    baseline: Literal["standard", "respiratory", "cardiovascular"] = "standard"
    available_from: int = Field(default=6, ge=0, le=23)
    available_until: int = Field(default=20, ge=1, le=24)
    activity_duration_hours: int = Field(default=1, ge=1, le=4)

    @model_validator(mode="after")
    def validate_window(self):
        self.display_name = self.display_name.strip()
        if not self.display_name:
            raise ValueError("Display name cannot be blank")
        if self.available_until - self.available_from < self.activity_duration_hours:
            raise ValueError("Available time must fit the full activity duration")
        if len(self.condition_ids) != len(set(self.condition_ids)):
            raise ValueError("Conditions must be unique")
        for values in (self.infectious_condition_ids, self.allergy_ids):
            if len(values) != len(set(values)):
                raise ValueError("Selections must be unique")
        return self

class Location(BaseModel):
    location_id: str
    city: str
    state: str
    latitude: float | None = None
    longitude: float | None = None

class ReferenceOption(BaseModel):
    id: str
    name: str
    group: str = "noncommunicable"

class Catalog(BaseModel):
    locations: list[Location]
    conditions: list[ReferenceOption]
    occupations: list[ReferenceOption]
    dates: list[str]
    infectious_conditions: list[ReferenceOption] = Field(default_factory=list)
    allergies: list[ReferenceOption] = Field(default_factory=list)

class WeatherHour(BaseModel):
    timestamp: str
    temperature_c: float
    relative_humidity_pct: float
    heat_index_c: float
    rainfall_mm_hr: float
    aqi: int | None = None
    uv_index: float | None = None
    wind_kmh: float
    pm2_5_ugm3: float | None = None
    weather_code: int | None = None
    cloud_cover: float | None = None
    is_day: bool = True
    apparent_temperature_c: float | None = None

class RiskResult(BaseModel):
    score: float
    level: Literal["Low", "Moderate", "High", "Severe"]
    dominant_hazard: Literal["none", "heat", "rain", "air_quality", "uv"]
    reasons: list[str]
    advice: list[str]

class ScoredHour(BaseModel):
    weather: WeatherHour
    risk: RiskResult

class TimeWindow(BaseModel):
    start: str
    end: str
    average_score: float
    level: str
    explanation: str

class Alert(BaseModel):
    id: str
    title: str
    message: str
    severity: str
    window_start: str
    window_end: str

class Dashboard(BaseModel):
    schema_version: str = "1.1"
    mode: str = "synthetic_demo"
    source: str = "Supplied synthetic Tamil Nadu dataset; not a live weather feed"
    timezone: str = "Asia/Kolkata"
    date: str
    location: Location
    profile: Profile
    focus_hour: ScoredHour
    daily_risk: RiskResult
    hours: list[ScoredHour]
    best_windows: list[TimeWindow]
    alerts: list[Alert]
    limitations: list[str]
    fetched_at: str | None = None
    valid_at: str | None = None
    sources: list[dict] = Field(default_factory=list)
    comparison: dict = Field(default_factory=dict)
    scene: str = "sunny"
    location_note: str = ""

class Coordinates(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

class Session(BaseModel):
    token: str
    profile: Profile
