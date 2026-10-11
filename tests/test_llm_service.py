from unittest.mock import AsyncMock, Mock

import pytest

from src.schema.tickets import TicketResponse, ValidTicketResponse
from src.services.llm_service import LLMService
from src.services.llm_settings import CREATE_TICKET_INSTRUCTIONS, MODEL


@pytest.mark.asyncio
async def test_generate_response():
    service = LLMService()
    service.client = Mock()

    expected_ticket = TicketResponse(
        result=ValidTicketResponse(
            category="account",
            priority="normal",
            summary="Der Nutzer kann sich nicht in seinem Konto anmelden.",
            order_id=None,
        )
    )

    service.client.responses.parse = AsyncMock(
        return_value=Mock(output_parsed=expected_ticket)
    )

    result = await service.generate_response("Login funktioniert nicht")

    assert result == expected_ticket

    service.client.responses.parse.assert_awaited_once_with(
        model=MODEL,
        input="Login funktioniert nicht",
        instructions=CREATE_TICKET_INSTRUCTIONS,
        text_format=TicketResponse,
    )
