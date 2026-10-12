from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TicketRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    request: str = Field(min_length=10, max_length=200)


class InvalidTicketResponse(BaseModel):
    category: Literal["invalid"]
    reason: str = Field(
        min_length=10,
        max_length=200,
        description="Begründung warum das Ticket als invalid eingestuft wurde",
    )


class ValidTicketResponse(BaseModel):
    category: Literal["billing", "technical", "account", "other"] = Field(
        description="Thema des Tickets"
    )
    priority: Literal["normal", "urgent"] = Field(
        description="urgent bei dringenden Problemen, sonst normal"
    )
    summary: str = Field(
        min_length=10,
        max_length=200,
        description="Kurze Zusammenfassung der Nutzereingabe",
    )
    order_id: str | None = Field(
        description="Bestellnummer aus der Eingabe; null, falls keine genannt wurde"
    )


class TicketResponse(BaseModel):
    result: InvalidTicketResponse | ValidTicketResponse
