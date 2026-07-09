import json
from datetime import datetime, timezone


def dumps_event(source, event_type, payload):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "event_type": event_type,
        "payload": payload,
    }
    return json.dumps(event, sort_keys=True)


def loads_event(raw):
    return json.loads(raw)
