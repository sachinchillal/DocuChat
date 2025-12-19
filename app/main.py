from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from services.gemini_service import explain_ai_briefly, get_all_caches, get_response_from_gemini
from services.data_service import get_chat_history, append_user_question_to_chat_history
from services.meeting_service import get_meetings
from fastapi.staticfiles import StaticFiles

# Load the .env file
load_dotenv()

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class MessageRequest(BaseModel):
    message: str
    meeting_id: int

@app.get("/api")
def read_root():
    return {"message": "Welcome to DocuChat"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/ai")
def explain_ai():
    """
    API endpoint that returns a brief explanation of how AI works,
    using the Gemini service.
    """
    explanation = explain_ai_briefly()
    return {"explanation": explanation}




@app.get("/ai/list_caches")
def list_caches():
    """
    API endpoint that lists all caches.
    """
    caches = get_all_caches()
    return {"caches": caches}

@app.get("/api/get_chat_history/{meeting_id}")
def get_chat_history_by_meeting_id_api(meeting_id: int):
    """
    API endpoint that gets the chat history.
    """
    chat_history = get_chat_history(meeting_id)
    return chat_history

@app.get("/api/get_meetings")
def get_meetings_api():
    """
    API endpoint that gets the meetings.
    """
    meetings = get_meetings()
    return meetings

@app.post("/api/send_message")
def send_message_api(request: MessageRequest):
    """
    API endpoint that sends a user message and gets AI response.
    """
    meeting_id = request.meeting_id
    message = request.message

    meetings = get_meetings()
    meeting = next((m for m in meetings if m['id'] == meeting_id), None)
    if not meeting:
        return {"error": "Meeting not found"}
    cached_content_name = meeting['cached_content_name']
    
    # Append user question to chat history
    chat_history = append_user_question_to_chat_history(meeting_id, message)
    
    # # Get AI response (this already appends the response to chat history internally)
    response = get_response_from_gemini(meeting_id, cached_content_name, chat_history)
    
    return {"status": "success", "message": "Message sent successfully", "data": response}


app.mount("/", StaticFiles(directory="public", html=True), name="public")
