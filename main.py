import logging

import requests

from src.config import API_KEY, BASE_TIMEOUT_SEC, BASE_URL, LLM_MAX_RETRIES

logger = logging.getLogger(__name__)


def main():
    user_request = input("Eingabe: ")

    try:
        response = requests.post(
            f"{BASE_URL}/tickets/",
            headers={"X-API-Key": API_KEY},
            json={"request": user_request},
            timeout=BASE_TIMEOUT_SEC * LLM_MAX_RETRIES,
        )

        response.raise_for_status()
        print(response.json())

    except requests.exceptions.Timeout:
        logger.exception("Zeitüberschreitung beim Request")
        raise


if __name__ == "__main__":
    main()
