import requests
import pytz
import argparse
from datetime import datetime, timedelta
from typing import Any, Dict, List
from patterns import patterns_tags

local_tz = 'America/Denver' # Set your timezone

def tag_event(event: Dict[str, Any], patterns_tags: List[tuple]) -> Dict[str, Any]:
    """Tag an event based on its 'App' and 'Title' using a list of regex patterns."""
    for pattern, tag in patterns_tags:
        if pattern.search(event["data"]["app"]) or pattern.search(event["data"]["title"]):
            event["tag"] = tag
            break
    return event

def query_bucket(bucket: str, date: str, local_tz: str) -> List[Dict[str, Any]]:
    """Fetch events for a given bucket and date from the server."""
    server_url, endpoint = "http://localhost:5600", f"/api/0/buckets/{bucket}/events"
    timezone = pytz.timezone(local_tz)
    start_date, end_date = timezone.localize(datetime.strptime(date, "%Y-%m-%d")), timezone.localize(datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1))
    url = f"{server_url}{endpoint}?start={start_date.isoformat()}&end={end_date.isoformat()}"
    response = requests.get(url, timeout=30)
    return response.json() if response.status_code == 200 else []

def find_bucket(bucket_prefix: str) -> str:
    """Find the bucket on the server with the specified prefix."""
    response = requests.get("http://localhost:5600/api/0/buckets/")
    return next((bucket for bucket in response.json() if bucket.startswith(bucket_prefix)), "") if response.status_code == 200 else ""

def filter_period_intersect(events1: List[Dict[str, Any]], events2: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter out events from the first list that intersect with any event in the second list."""
    events1.sort(key=lambda event: event["timestamp"])
    events2.sort(key=lambda event: event["timestamp"])
    result = []
    index1, index2 = 0, 0
    while index1 < len(events1) and index2 < len(events2):
        if events1[index1]["timestamp"] < events2[index2]["timestamp"]:
            result.append(events1[index1])
            index1 += 1
        else:
            index2 += 1
    result.extend(events1[index1:])
    return result

def merge_events_by_keys(events: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    """Merge events that have same values for the specified keys."""
    merged_events = []
    for event in events:
        for merged_event in merged_events:
            if all(event["data"].get(key) == merged_event["data"].get(key) for key in keys):
                merged_event["duration"] += event["duration"]
                break
        else:
            merged_events.append(event)
    return merged_events

def filter_keyvals(events: List[Dict[str, Any]], key: str, values: List[Any]) -> List[Dict[str, Any]]:
    """Filter events based on values of a specific key."""
    return [event for event in events if event["data"].get(key) in values]

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="The date for which to query events in format YYYY-MM-DD")
    args = parser.parse_args()
    date = args.date

    afk_bucket = find_bucket("aw-watcher-afk_")
    window_bucket = find_bucket("aw-watcher-window_")
    afk_events = query_bucket(afk_bucket, date, local_tz)
    window_events = query_bucket(window_bucket, date, local_tz)
    window_events = filter_period_intersect(window_events, filter_keyvals(afk_events, "status", ["not-afk"]))
    merged_events = merge_events_by_keys(window_events, ["app", "title"])
    local_tz_obj = pytz.timezone(local_tz)

    print("Timestamp,Duration (min),App,Title,Tag")
    for event in merged_events:
        if event['duration'] > 0.0:
            timestamp = datetime.fromisoformat(event['timestamp'].replace("Z", "+00:00"))
            local_timestamp = timestamp.astimezone(local_tz_obj).strftime('%Y-%m-%d %H:%M')
            duration_minutes = round(event['duration'] / 60, 1)
            title = event['data']['title'][:32]
            
            event = tag_event(event, patterns_tags)
            print(f"{local_timestamp},{duration_minutes},{event['data']['app']},{title},{event.get('tag', '')}")


if __name__ == "__main__":
    main()
