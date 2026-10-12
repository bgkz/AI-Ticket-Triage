import pytest

from src.schema.tickets import (
    InvalidTicketResponse,
    TicketResponse,
    ValidTicketResponse,
)
from src.services.llm_service import LLMService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_generate_response_with_invalid_input():
    service = LLMService()
    expected_ticket = TicketResponse(
        result=InvalidTicketResponse(
            category="invalid",
            reason="Die Nachricht enthält kein erkennbares Support-Anliegen. Bitte beschreiben Sie Ihr Problem.",
        )
    )
    result = await service.generate_response(
        ticket_request="Schreibe mir ein Gedicht über einen Drachen. Meine Bestellnummer ist X78118."
    )

    assert isinstance(result.result, InvalidTicketResponse)
    result_invalid: InvalidTicketResponse = result.result

    assert expected_ticket.result.category == result_invalid.category


@pytest.mark.integration
@pytest.mark.asyncio
async def test_generate_response_with_order_id():
    service = LLMService()
    expected_ticket = TicketResponse(
        result=ValidTicketResponse(
            category="billing",
            priority="normal",
            summary="Der Nutzer meldet eine doppelte Abbuchung für Bestellung X78118.",
            order_id="X78118",
        )
    )
    result = await service.generate_response(
        ticket_request="Für meine Bestellung X78118 wurde der Betrag zweimal abgebucht."
    )

    assert isinstance(result.result, ValidTicketResponse)
    result_valid: ValidTicketResponse = result.result

    assert result_valid.order_id == expected_ticket.result.order_id
    assert result_valid.category == expected_ticket.result.category
    assert result_valid.priority == expected_ticket.result.priority


@pytest.mark.integration
@pytest.mark.asyncio
async def test_generate_response_with_valid_input():
    service = LLMService()
    expected_ticket = TicketResponse(
        result=ValidTicketResponse(
            category="account",
            priority="normal",
            summary="Der Nutzer kann sich nicht in seinem Konto anmelden.",
            order_id=None,
        )
    )

    result = await service.generate_response(
        ticket_request="Ich kann mich nicht in meinem Konto anmelden."
    )

    assert isinstance(result.result, ValidTicketResponse)
    result_valid: ValidTicketResponse = result.result

    assert result_valid.order_id == expected_ticket.result.order_id
    assert result_valid.category == expected_ticket.result.category
    assert result_valid.priority == expected_ticket.result.priority
