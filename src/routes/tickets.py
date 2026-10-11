import openai
from fastapi import APIRouter, Depends, HTTPException, status

from src.schema.tickets import TicketRequest
from src.security.api_key import verify_api_key
from src.services.llm_service import LLMService

router = APIRouter(
    prefix="/tickets",
    dependencies=[Depends(verify_api_key)],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_request: TicketRequest):
    try:
        return await LLMService().generate_response(
            ticket_request=ticket_request.request
        )

    except openai.AuthenticationError as error:
        raise HTTPException(
            status_code=500,
            detail="Authentifizierung beim KI-Dienst fehlgeschlagen",
        ) from error
