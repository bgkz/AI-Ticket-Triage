import openai

from src.config import BASE_TIMEOUT_SEC, OPENAI_API_KEY
from src.schema.tickets import TicketResponse
from src.services.llm_settings import CREATE_TICKET_INSTRUCTIONS, MODEL


class LLMService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            max_retries=2,
            timeout=BASE_TIMEOUT_SEC,
        )

    async def generate_response(self, ticket_request: str) -> TicketResponse:
        response = await self.client.responses.parse(
            model=MODEL,
            input=ticket_request,
            instructions=CREATE_TICKET_INSTRUCTIONS,
            text_format=TicketResponse,
        )

        return response.output_parsed
