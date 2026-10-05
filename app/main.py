from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Load the .env file
load_dotenv()

from api.routers.ai import router as ai_router
from api.routers.chat import router as chat_router
from api.routers.items import router as items_router
from api.routers.meetings import router as meetings_router
from api.routers.root import router as root_router


def create_app() -> FastAPI:
    app = FastAPI()

    # API routers (grouped endpoints)
    app.include_router(root_router)
    app.include_router(ai_router)
    app.include_router(meetings_router)
    app.include_router(chat_router)
    app.include_router(items_router)

    # Static frontend
    app.mount("/", StaticFiles(directory="public", html=True), name="public")

    return app


app = create_app()
