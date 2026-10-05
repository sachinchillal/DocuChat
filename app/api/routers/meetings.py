from fastapi import APIRouter

from services.meeting_service import get_meetings

router = APIRouter(prefix="/api", tags=["meetings"])


@router.get("/get_meetings")
def get_meetings_api():
    """
    API endpoint that gets the meetings.
    """
    meetings = get_meetings()
    return meetings

