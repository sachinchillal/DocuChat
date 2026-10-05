from fastapi import APIRouter

from services.gemini_service import explain_ai_briefly, get_all_caches

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("")
def explain_ai():
    """
    API endpoint that returns a brief explanation of how AI works,
    using the Gemini service.
    """
    explanation = explain_ai_briefly()
    return {"explanation": explanation}


@router.get("/list_caches")
def list_caches():
    """
    API endpoint that lists all caches.
    """
    caches = get_all_caches()
    return {"caches": caches}

