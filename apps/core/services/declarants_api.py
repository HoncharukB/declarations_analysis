import requests

from apps.core.models import Declarant


class DeclarationsService:
    API_URL = "https://public-api.nazk.gov.ua/v2/documents/list"

    @classmethod
    def find_declarant(cls, *, lastname: str = "", firstname: str = "", middlename: str = "",
                       user_declarant_id: str = ""):
        """Шукає декларантів через API НАЗК"""
        response = requests.get(
            f"{cls.API_URL}?query={f"{lastname} {firstname} {middlename}".strip()} "
            f"{f"&user_declarant_id={user_declarant_id}" if user_declarant_id else ""}",
            timeout=5
        )
        if response.status_code != 200:
            return []

        response.raise_for_status()
        api_dictionary = response.json()

        # Кількість знайдених декларацій
        count = api_dictionary.get('count', 0)

        results = []
        for declaration in api_dictionary.get("data", []):
            step1 = declaration.get("data", {}).get("step_1", {}).get("data", {})
            results.append(
                Declarant(
                    lastname=step1.get("lastname", ""),
                    firstname=step1.get("firstname", ""),
                    middlename=step1.get("middlename", ""),
                    user_declarant_id=declaration.get("user_declarant_id", "")
                )
            )
        return results, count