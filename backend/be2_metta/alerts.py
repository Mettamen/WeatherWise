"""Metta: group adjacent elevated-risk hours; cap the in-app list."""
from datetime import datetime, timedelta
import hashlib
from shared.contracts import Alert, ScoredHour

def build_alerts(hours: list[ScoredHour], location_id: str) -> list[Alert]:
    groups = []
    for hour in hours:
        if hour.risk.score < 25:
            continue
        timestamp = datetime.fromisoformat(hour.weather.timestamp)
        if groups and groups[-1][-1].risk.dominant_hazard == hour.risk.dominant_hazard and datetime.fromisoformat(groups[-1][-1].weather.timestamp) + timedelta(hours=1) == timestamp:
            groups[-1].append(hour)
        else:
            groups.append([hour])
    alerts = []
    for group in groups:
        peak = max(group, key=lambda h: h.risk.score)
        start = group[0].weather.timestamp
        end = (datetime.fromisoformat(group[-1].weather.timestamp) + timedelta(hours=1)).isoformat()
        key = f"{location_id}:{start}:{end}:{peak.risk.score}:{peak.risk.dominant_hazard}"
        alerts.append(Alert(id=hashlib.sha256(key.encode()).hexdigest()[:16], title=f"{peak.risk.level} {peak.risk.dominant_hazard.replace('_', ' ')} risk",
            severity=peak.risk.level, message=peak.risk.advice[0], window_start=start, window_end=end))
    return sorted(alerts, key=lambda a: (a.window_start, a.id))[:8]
