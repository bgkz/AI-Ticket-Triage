import pytest
from pydantic import ValidationError

from src.schema.tickets import (
    InvalidTicketResponse,
    TicketRequest,
    TicketResponse,
    ValidTicketResponse,
)


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
