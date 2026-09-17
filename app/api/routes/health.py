from fastapi import APIRouter, Request

from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health(request: Request) -> dict[str, str | bool]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "llm_provider": settings.llm_provider.value,
        "llm_configured": request.app.state.llm_config_error is None,
    }
