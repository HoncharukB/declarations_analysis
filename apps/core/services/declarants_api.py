import html
from datetime import datetime

import requests

from apps.core.models.declaration import DeclarationType, DocumentType


class DeclarationsService:
    API_URL = "https://public-api.nazk.gov.ua/v2/documents/list"

    @classmethod
    def find_declarant(cls, *, lastname: str = "", firstname: str = "", middlename: str = "",
                       user_declarant_id: str = "", page: int = 1, per_page: int = 100):
        # пошук за ПІБ та ID декларанта
        params = {"page": page, "per_page": per_page}
        # пошук за прізвищем або іменем або по батькові
        if lastname or firstname or middlename:
            params["query"] = f"{lastname} {firstname} {middlename}".strip()
        # пошук за ID декларанта
        if user_declarant_id:
            params["user_declarant_id"] = user_declarant_id

        response = requests.get(cls.API_URL, params=params, timeout=5)

        if response.status_code != 200:
            return []

        response.raise_for_status()
        api_dictionary = response.json()

        # Кількість знайдених декларацій
        count = api_dictionary.get('count', 0)

        results = []
        for declaration in api_dictionary.get("data", []):
            step1 = declaration.get("data", {}).get("step_1", {}).get("data", {})
            step0 = declaration.get("data", {}).get("step_0", {}).get("data", {})

            # Дата
            raw_date = declaration.get("date", "")
            formatted_date = ""
            if raw_date:
                try:
                    formatted_date = datetime.fromisoformat(raw_date).strftime("%d.%m.%Y %H:%M")
                except Exception:
                    formatted_date = raw_date

            # Тип документу (mapping з choices)
            document_type_code = declaration.get("type", None)
            try:
                doc_type_code = int(document_type_code) if document_type_code is not None else None
            except ValueError:
                doc_type_code = None

            document_type_display = dict(DocumentType.choices).get(doc_type_code, "")

            # Тип декларації (mapping з choices)
            type_code = declaration.get("declaration_type", None)
            try:
                type_code = int(type_code) if type_code is not None else None
            except ValueError:
                type_code = None

            type_display = dict(DeclarationType.choices).get(type_code, "")

            # Період
            year = str(step0.get("declaration_year", "")).strip()
            period = str(step0.get("declaration_period", "")).strip()

            display_period = f"{year} ({period})" if period != year else year

            results.append({
                "document_id": declaration.get("id"),
                "lastname": step1.get("lastname", ""),
                "firstname": step1.get("firstname", ""),
                "middlename": step1.get("middlename", ""),
                "user_declarant_id": declaration.get("user_declarant_id", ""),
                "work_place": html.unescape(step1.get("workPlace", "")),
                "work_post": html.unescape(step1.get("workPost", "")),

                # поля декларації
                "document_type_display": document_type_display,
                "declaration_year": year,
                "declaration_type_display": type_display,
                "declaration_period": display_period,
                "date": formatted_date,
            })

        return results, count