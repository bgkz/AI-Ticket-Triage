import openai
from fastapi import APIRouter, Depends, HTTPException, status

from src.schema.tickets import TicketRequest
from src.security.api_key import verify_api_key
from src.services.exceptions import MissingStructuredResponseError
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

    except openai.APITimeoutError as error:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Zeitüberschreitung beim KI-Dienst. Bitte versuchen Sie es später erneut.",
        ) from error

    except MissingStructuredResponseError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Der KI-Dienst hat keine gültige Antwort geliefert. Bitte versuchen Sie es erneut.",
        ) from error
