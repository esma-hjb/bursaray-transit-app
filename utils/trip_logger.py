import json
from datetime import datetime

FILE_PATH = "data/trips_history.json"


def save_trip(trip):
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    except:
        data = []

    record = {
        "from": trip.steps[0].from_stop_id if trip.steps else None,
        "to": trip.steps[-1].to_stop_id if trip.steps else None,
        "duration": trip.total_duration_min,
        "fare": trip.total_fare,
        "steps": [
            {
                "mode": s.mode,
                "from": s.from_stop_id,
                "to": s.to_stop_id
            }
            for s in trip.steps
        ],
        "timestamp": str(datetime.now())
    }

    data.append(record)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_trips():
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return []