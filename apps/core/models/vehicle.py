from django.db import models
from apps.core.models.validators.validators import validate_other_ownership


class VehicleType(models.TextChoices):
    PASSENGER_CAR = "Автомобіль легковий", "Автомобіль легковий"
    TRUCK = "Автомобіль вантажний", "Автомобіль вантажний"
    BUS = "Автобус", "Автобус"
    TRAILER = "Причіп", "Причіп"
    SEMI_TRAILER = "Напівпричіп", "Напівпричіп"
    MOTORCYCLE = "Мотоцикл", "Мотоцикл"
    MOPED = "Мопед", "Мопед"
    TRICYCLE = "Трицикл", "Трицикл"
    QUADRICYCLE = "Квадроцикл", "Квадроцикл"
    AGRICULTURAL_MACHINE = "Сільськогосподарська техніка", "Сільськогосподарська техніка"
    WATERCRAFT = "Водний засіб", "Водний засіб"
    AIRCRAFT = "Повітряний засіб", "Повітряний засіб"
    OTHER = "Інше", "Інше"

class OwnerShipType(models.TextChoices):
    OWNERSHIP = "Власність", "Власність"
    JOINT_OWNERSHIP = "Спільна сумісна власність", "Спільна сумісна власність"
    PARTIAL_OWNERSHIP = "Спільна часткова власність", "Спільна часткова власність"
    RENT = "Оренда", "Оренда"
    POSSESSION_WITHOUT_USE = "Перебуває у володінні (без права користування)", "Перебуває у володінні (без права користування)"
    OTHER_USAGE_RIGHT = "Інше право користування", "Інше право користування"

class Vehicle(models.Model):
    # Звичайні поля
    iteration = models.CharField(max_length=100) # id транспортного засобу з API НАЗК
    object_type = models.CharField(max_length=100, choices=VehicleType.choices, null=True, blank=True) # Вид транспортного засобу
    brand = models.CharField(max_length=100, null=True, blank=True) # марка
    model = models.CharField(max_length=100, null=True, blank=True) # модель
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True) # рік випуску
    cost_date = models.CharField(max_length=100, null=True, blank=True) # вартість на дату набуття
    owning_date = models.CharField(max_length=100, null=True, blank=True) # дата набуття
    ownerShip = models.CharField(max_length=100, choices=OwnerShipType.choices, null=True, blank=True) # тип права
    otherOwnership = models.CharField(max_length=255, null=True, blank=True) # яке інше право користування
    # Зв'язки
    declarations = models.ManyToManyField("Declaration", related_name='vehicles')
    owners = models.ManyToManyField("Owner", related_name='vehicles')
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        validate_other_ownership(self)

    def __str__(self):
        parts = []
        if self.brand:
            parts.append(self.brand)
        if self.model:
            parts.append(self.model)
        if self.object_type and hasattr(self, "get_object_type_display"):
            parts.append(f"({self.get_object_type_display()})")
        elif self.object_type:
            parts.append(f"({self.object_type})")
        if self.ownerShip and hasattr(self, "get_ownerShip_display"):
            parts.append(f"Тип права: {self.get_ownerShip_display()}")
        elif self.ownerShip:
            parts.append(f"Тип права: {self.ownerShip}")
        if self.otherOwnership:
            parts.append(f"Додатково: {self.otherOwnership}")
        return " ".join(parts) if parts else f"Транспортний засіб {self.iteration}"