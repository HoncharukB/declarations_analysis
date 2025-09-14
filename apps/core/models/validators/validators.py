from django.core.exceptions import ValidationError

def validate_other_ownership(instance):
    from apps.core.models.vehicle import OwnerShipType
    if instance.ownerShip == OwnerShipType.OTHER_USAGE_RIGHT:
        if not instance.otherOwnership:
            raise ValidationError(
                {"otherOwnership": "Це поле обов’язкове, коли вибрано 'Інше право користування'."}
            )
    else:
        if instance.otherOwnership:
            raise ValidationError(
                {"otherOwnership": "Це поле має бути порожнім, якщо не вибрано 'Інше право користування'."}
            )

def validate_owner_fields(instance):
    from apps.core.models.owner import OwnerType, CitizenType

    errors = {}
    if instance.owner_type == OwnerType.PERSON:
        missing_fields = [field for field in ['last_name', 'first_name'] if not getattr(instance, field)]
        if missing_fields:
            errors['missing_fields'] = ValidationError(
                f"Для власника - третьої особи, поля {', '.join(missing_fields)} обов’язкові."
            )
        for field in ['company_name', 'company_code']:
            if getattr(instance, field):
                errors[field] = ValidationError(
                    f"Поле {field} має бути порожнім для власника типу Третя особа."
                )
        if instance.citizen not in [CitizenType.UKRAINIAN_CITIZEN, CitizenType.FOREIGN_CITIZEN]:
            errors['citizen'] = ValidationError(
                "Для власника типу 'Третя особа' оберіть 'Громадянин України' або 'Іноземний громадянин'."
            )
    elif instance.citizen in [CitizenType.UKRAINIAN_LEGAL_ENTITY, CitizenType.FOREIGN_LEGAL_ENTITY]:
        for field in ['company_name', 'company_code']:
            if not getattr(instance, field):
                errors[field] = ValidationError(
                    f"Поле {field} є обов’язковим для юридичної особи."
                )
        for field in ['last_name', 'first_name', 'middle_name']:
            if getattr(instance, field):
                errors[field] = ValidationError(
                    f"Поле {field} має бути порожнім для юридичної особи."
                )
    if errors:
        raise ValidationError(errors)