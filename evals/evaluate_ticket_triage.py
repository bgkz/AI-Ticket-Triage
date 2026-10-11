import asyncio
import json
import logging
from pathlib import Path

from src.services.llm_service import LLMService

logger = logging.getLogger(__name__)


async def main():
    with Path(__file__).with_name("cases.json").open(encoding="utf-8") as file:
        cases = json.load(file)

    llm_service = LLMService()

    try:
        evaluation_results: list[dict] = []
        for case in cases:
            case_id = case["id"]
            request = case["request"]
            expected = case["expected"]
            checks = case["checks"]

            actual = None
            field_checks = {}
            error = None

            try:
                ticket_response = await llm_service.generate_response(
                    ticket_request=request
                )

                if ticket_response is None:
                    raise RuntimeError("Keine strukturierte Antwort erhalten")

                logger.info("Fall %s wird ausgewertet", case_id)
                logger.debug("Eingabe: %s", request)
                logger.info("Antworttyp: %s", type(ticket_response.result).__name__)

                actual = ticket_response.result.model_dump(mode="json")
                field_checks = {
                    field: field in actual and actual[field] == expected_value
                    for field, expected_value in expected.items()
                }
                evaluation_status = "passed" if all(field_checks.values()) else "failed"
            except Exception as exc:
                logger.exception("Fehler bei Fall %s", case_id)
                evaluation_status = "error"
                error = {"type": type(exc).__name__, "message": str(exc)}

            evaluation_results.append(
                {
                    "case_id": case_id,
                    "request": request,
                    "expected": expected,
                    "actual": actual,
                    "checks": field_checks,
                    "review_notes": checks,
                    "status": evaluation_status,
                    "error": error,
                }
            )

        output_path = Path(__file__).with_name("evaluation_results.json")

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(evaluation_results, file, ensure_ascii=False, indent=2)

        logger.info("Evaluation Ergebnisse gespeichert: %s", output_path)

    finally:
        await llm_service.client.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    asyncio.run(main())
