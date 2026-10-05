from fastapi import APIRouter

router = APIRouter(tags=["root"])


@router.get("/api")
def read_root():
    return {"message": "Welcome to DocuChat"}

