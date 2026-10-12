from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from openai import AuthenticationError

from src.main import app
from src.schema.tickets import (
    InvalidTicketResponse,
    TicketResponse,
    ValidTicketResponse,
)

client = TestClient(app)


@pytest.mark.parametrize("key", ["invalid API KEY", None])
def test_endpoint_with_invalid_API_KEY(key: str | None):
    headers = {"X-API-Key": key} if key is not None else {}

    response = client.post(
        "/tickets/",
        json={"request": "Ich kann mich nicht in meinem Konto anmelden."},
        headers=headers,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "API-Key missing or invalid"


def test_enpoint_with_authentication_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.security.api_key.API_KEY", "test-api-key")
    error = AuthenticationError(
        message="Invalid API key",
        response=httpx.Response(
            status_code=401,
            request=httpx.Request("POST", "https://api.openai.com/v1/responses"),
        ),
        body=None,
    )
    service = Mock()
    service.generate_response = AsyncMock(side_effect=error)

    monkeypatch.setattr(
        "src.routes.tickets.LLMService",
        Mock(return_value=service),
    )
    response = client.post(
        "/tickets/",
        json={"request": "Ich kann mich nicht in meinem Konto anmelden."},
        headers={"X-API-Key": "test-api-key"},
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        response.json()["detail"] == "Authentifizierung beim KI-Dienst fehlgeschlagen"
    )


def test_endpoint_with_valid_request(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.security.api_key.API_KEY", "test-api-key")

    service = Mock()
    expected_ticket = TicketResponse(
        result=ValidTicketResponse(
            category="account",
            priority="normal",
            summary="Der Nutzer kann sich nicht in seinem Konto anmelden. Bestellnummer: XX-4421.",
            order_id="XX-4421",
        )
    )

    service.generate_response = AsyncMock(return_value=expected_ticket)

    monkeypatch.setattr(
        "src.routes.tickets.LLMService",
        Mock(return_value=service),
    )

    response = client.post(
        "/tickets/",
        json={
            "request": "Ich kann mich nicht in meinem Konto anmelden. Bestellnummer XX-4421"
        },
        headers={"X-API-Key": "test-api-key"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_ticket.model_dump(mode="json")


def test_endpoint_with_invalid_request(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.security.api_key.API_KEY", "test-api-key")

    service = Mock()
    expected_ticket = TicketResponse(
        result=InvalidTicketResponse(
            category="invalid",
            reason="Die Anfrage ist eine kreative Aufgabe ohne Supportbezug. Bitte beschreiben Sie Ihr Problem.",
        )
    )

    service.generate_response = AsyncMock(return_value=expected_ticket)

    monkeypatch.setattr(
        "src.routes.tickets.LLMService",
        Mock(return_value=service),
    )

    response = client.post(
        "/tickets/",
        json={
            "request": "Schreibe mir ein Gedicht über einen Drachen. Meine Bestellnummer ist XX-4421."
        },
        headers={"X-API-Key": "test-api-key"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_ticket.model_dump(mode="json")
