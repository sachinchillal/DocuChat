import os
import json
from google import genai
from google.genai.types import CreateCachedContentConfig,GenerateContentConfig,CachedContent
from google.genai.errors import ClientError
from pydantic import BaseModel
from services.data_service import append_model_response_to_chat_history
from services.meeting_service import update_meeting_cache_name

gemini_api_key = os.getenv("GEMINI_API_KEY", "GEMINI_API_KEY")
gemini_model = "gemini-2.5-flash"

client = genai.Client(api_key=gemini_api_key)


def explain_ai_briefly() -> str:
    """
    Call Gemini to get a brief explanation of how AI works.
    """
    response = client.models.generate_content(
        model=gemini_model,
        contents="Explain how AI works in a few words",
    )
    if response.text is None:
        return "No response from Gemini"
    return response.text

def get_transcripts_from_my_db(meeting_id: int):
    f = f"data/meeting_{meeting_id}.txt"
    with open(f, 'r') as file:
        return file.read()

def create_cached_content(meeting_id: int):
    # 1. Retrieve durable data
    full_transcript = get_transcripts_from_my_db(meeting_id)
    # print(full_transcript)
    
    # 2. Create an ephemeral cache for this active session
    # We set a TTL (Time To Live) of 1 hour (3600 seconds)
    cache = client.caches.create(
        model=gemini_model,
        config=CreateCachedContentConfig(
                display_name=get_cache_display_name(meeting_id),
                system_instruction="You are a helpful assistant answering questions about these meetings.",
                contents=[full_transcript],
                ttl='3600s',  # 1 hour in seconds
        ),
    )
    if cache is not None:
        # save the cached content name to the meeting
        update_meeting_cache_name(meeting_id, cache.name or "")
    print(cache)
    return cache

def get_cache_display_name(meeting_id: int) -> str:
    return f"session_{meeting_id}"

def get_cached_content(meeting_id: int, cached_content_name: str) -> CachedContent | None:
    try:
        if cached_content_name == "":
            print("Cached content name is empty, creating new cache...")
            return create_cached_content(meeting_id)
            
        return client.caches.get(name=cached_content_name)

    except ClientError as e:
        # Check if it's a 403 PERMISSION_DENIED error (cache not found)
        m = "CachedContent not found (or permission denied)"
        c = 403
        if e.message == m and e.code == c:
            print("CachedContent not found (or permission denied), creating new cache...")
            return create_cached_content(meeting_id)
        else:
            return None
    except Exception as e:
        print(f"Unexpected error getting cached content: {e}")
        return None

class EmailSchema(BaseModel):
    subject: str
    body: str

def get_response_from_gemini(meeting_id: int, cached_content_name: str, chat_history: list[dict]) -> dict:
    # Create a chat session that uses the cached content as context
    cache = get_cached_content(meeting_id, cached_content_name)
    if cache is None:
        return {"error": "CachedContent not found (or permission denied)"}
    
    cached_content_name = cache.name or ""
    if not cached_content_name:
        return {"error": "Unable to cache context"}
    response = client.models.generate_content(
        model=gemini_model,
        contents=chat_history,
        config=GenerateContentConfig(cached_content=cached_content_name,
                 response_mime_type="application/json",
                 response_schema=EmailSchema,
        ),
    )
    if response.text and response.text.strip():
        try:
            append_model_response_to_chat_history(meeting_id, response.text)
            parsed = json.loads(response.text)
            if parsed:  # ensure JSON not empty
                print(parsed)
                return parsed
        except Exception:
            # invalid JSON → retry
            return {"error": "Invalid JSON"}
    return {"error": "No response from Gemini"}


def get_all_caches() -> list[CachedContent]:
    caches = client.caches.list()
    print(caches)
    return [cache for cache in caches]