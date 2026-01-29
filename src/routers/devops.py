from fastapi import APIRouter, Depends
from core.security import validate_auth_headers
from schemas.message import MessageRequest, MessageResponse
from services.message_service import MessageService

router = APIRouter()


@router.post(
    "/DevOps", 
    response_model=MessageResponse,
    dependencies=[Depends(validate_auth_headers)]
)
async def devops_endpoint(message_in: MessageRequest):
    return MessageService.process_message(message_in)
