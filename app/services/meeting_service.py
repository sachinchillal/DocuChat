import json

meetings_file = "data/meetings.json"

def update_meeting_cache_name(meeting_id: int, cached_content_name: str) -> list[dict]:
    # get the meetings
    meetings = get_meetings()
    # update the cached content name
    meetings[meeting_id-1]['cached_content_name'] = cached_content_name
    # save the meetings
    save_meetings(meetings)
    return meetings

def save_meetings(meetings: list[dict]) -> None:
    # save the meetings to the file
    with open(meetings_file, 'w') as file:
        json.dump(meetings, file)

def get_meetings() -> list[dict]:
    # get the meetings from the file
    with open(meetings_file, 'r') as file:
        meetings = json.load(file)
    return meetings
