import openai

from src.config import BASE_TIMEOUT_SEC, LLM_MAX_RETRIES, OPENAI_API_KEY
from src.schema.tickets import TicketResponse
from src.services.exceptions import MissingStructuredResponseError
from src.services.llm_settings import CREATE_TICKET_INSTRUCTIONS, MODEL


class LLMService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            max_retries=LLM_MAX_RETRIES,
            timeout=BASE_TIMEOUT_SEC,
        )

    async def generate_response(self, ticket_request: str) -> TicketResponse:
        response = await self.client.responses.parse(
            model=MODEL,
            input=ticket_request,
            instructions=CREATE_TICKET_INSTRUCTIONS,
            text_format=TicketResponse,
        )

        if response.output_parsed is None:
            raise MissingStructuredResponseError("Keine strukturierte Antwort erhalten")
        return response.output_parsed
