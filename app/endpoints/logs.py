from fastapi import APIRouter
from app.utils import logger

router = APIRouter()

@router.post("/")
def log_action(endpoint: str, data: dict):
    logger.log_request(endpoint, data)
    return {"message": "Log recorded"}
