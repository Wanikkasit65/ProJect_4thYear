mock_recent_runs = [
    {
        "date": "2024-10-05",
        "type": "Tempo",
        "distance_km": 10.5,
        "pace_min_per_km": 4.45,
        "duration_min": 47,
        "hr_zones": {"zone1": 2, "zone2": 5, "zone3": 10, "zone4": 25, "zone5": 5}  # minutes
    },
    {
        "date": "2024-10-03",
        "type": "Easy",
        "distance_km": 8.0,
        "pace_min_per_km": 5.20,
        "duration_min": 42,
        "hr_zones": {"zone1": 10, "zone2": 20, "zone3": 8, "zone4": 4, "zone5": 0}
    },
    {
        "date": "2024-10-01",
        "type": "Interval",
        "distance_km": 12.0,
        "pace_min_per_km": 4.10,
        "duration_min": 50,
        "hr_zones": {"zone1": 1, "zone2": 3, "zone3": 12, "zone4": 28, "zone5": 6}
    }
]

mock_30day_avg = {
    "distance_km": 9.5,
    "pace_min_per_km": 4.60,
    "hr_zone4_min": 18
}

def get_mock_data(user_id: str):
    return {
        "user_id": user_id,
        "recent_runs": mock_recent_runs,
        "avg_30day": mock_30day_avg
    }

