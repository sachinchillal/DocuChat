from fastapi import APIRouter
from pydantic import BaseModel

from services.data_service import (
    append_user_question_to_chat_history,
    get_chat_history,
)
from services.gemini_service import get_response_from_gemini
from services.meeting_service import get_meetings

router = APIRouter(prefix="/api", tags=["chat"])


class MessageRequest(BaseModel):
    message: str
    meeting_id: int


@router.get("/get_chat_history/{meeting_id}")
def get_chat_history_by_meeting_id_api(meeting_id: int):
    """
    API endpoint that gets the chat history.
    """
    chat_history = get_chat_history(meeting_id)
    return chat_history


@router.post("/send_message")
def send_message_api(request: MessageRequest):
    """
    API endpoint that sends a user message and gets AI response.
    """
    meeting_id = request.meeting_id
    message = request.message

    meetings = get_meetings()
    meeting = next((m for m in meetings if m["id"] == meeting_id), None)
    if not meeting:
        return {"error": "Meeting not found"}

    cached_content_name = meeting["cached_content_name"]

    # Append user question to chat history
    chat_history = append_user_question_to_chat_history(meeting_id, message)

    # Get AI response (this already appends the response to chat history internally)
    response = get_response_from_gemini(meeting_id, cached_content_name, chat_history)

    return {"status": "success", "message": "Message sent successfully", "data": response}

