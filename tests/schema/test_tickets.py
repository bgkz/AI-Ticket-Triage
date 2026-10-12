import pytest
from pydantic import ValidationError

from src.schema.tickets import (
    InvalidTicketResponse,
    TicketRequest,
    TicketResponse,
    ValidTicketResponse,
)


@pytest.mark.parametrize("category", ["", "weird", " ba ng"])
def test_invalid_ticket_response_with_invalid_categories(category: str) -> None:
    with pytest.raises(ValidationError):
        InvalidTicketResponse(
            category=category,
            reason="Die Nachricht enthält kein erkennbares Support-Anliegen.",
        )


@pytest.mark.parametrize("length", [10, 200])
def test_invalid_ticket_response_valid_reason_length(length: int) -> None:
    ticket = InvalidTicketResponse(category="invalid", reason="a" * length)

    assert ticket.reason == "a" * length


@pytest.mark.parametrize(
    ("length", "error_type"),
    [(0, "string_too_short"), (9, "string_too_short"), (201, "string_too_long")],
)
def test_invalid_ticket_response_invalid_reason_length(
    length: int, error_type: str
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        InvalidTicketResponse(category="invalid", reason="a" * length)

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["loc"] == ("reason",)
    assert errors[0]["type"] == error_type


def test_invalid_ticket_response_field_required() -> None:
    with pytest.raises(ValidationError) as exc_info:
        InvalidTicketResponse(category="invalid")

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["loc"] == ("reason",)
    assert errors[0]["type"] == "missing"


@pytest.mark.parametrize("length", [10, 200])
def test_ticket_request_valid_length(length: int):
    ticket = TicketRequest(request="a" * length)

    assert ticket.request == "a" * length


@pytest.mark.parametrize("length", [0, 9, 201])
def test_ticket_request_invalid_length(length: int):
    with pytest.raises(ValidationError):
        TicketRequest(request="a" * length)


def test_ticket_request_strips_whitespace():
    ticket = TicketRequest(request="  Login funktioniert nicht  ")

    assert ticket.request == "Login funktioniert nicht"


def test_ticket_request_validates_length_after_stripping():
    with pytest.raises(ValidationError):
        TicketRequest(request="  abc  ")
