import random
import unittest
import uuid

from django.db.models import UUIDField

from apps.core.models import Declarant

"""    # Id
    user_declarant_id = models.PositiveIntegerField(unique=True)
    api_id = models.UUIDField(unique=True, null=True, blank=True)
    # Звичайні поля
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    work_place = models.CharField(max_length=255, null=True, blank=True)
    work_post = models.CharField(max_length=255, null=True, blank=True)"""

# Test Case - Набір тестів
class DeclarantModelTest(unittest.TestCase):
    # Pre Condition Запускається перед кожним тестом
    # Створення тестового клієнта перед кожним тестом
    def setUp(self):
        self.declarant_data={
            'user_declarant_id': random.randint(10,1000),
            'api_id': uuid.uuid4(),
            'surname':'Stepnenko',
            'name':'Petro',
            'patronymic':'Ivanovich',
            'work_place':'IT Step',
            'work_post':'developer',
        }
        # Створення об'єкту, запис об'єкта в таблицю бази даних, присвоєння id об'єкту
        self.declarant=Declarant.objects.create(**self.declarant_data)

    # Test - Метод - Окремий тест
    # Перевірка чи вірно створився декларант в таблиці
    def test_create_declarant(self):
        declarant = Declarant.objects.get(id=self.declarant.id)
        print(declarant)
        # Перевірка даних
        self.assertEqual(declarant.surname, self.declarant_data['surname'])
        self.assertEqual(declarant.name, self.declarant_data['name'])
        self.assertEqual(declarant.patronymic, self.declarant_data['patronymic'])
        self.assertEqual(declarant.work_place, self.declarant_data['work_place'])
        self.assertEqual(declarant.work_post, self.declarant_data['work_post'])

    def test_update_declarant(self):
        self.declarant.surname = "Petrov"
        self.declarant.name = "Vasil"
        #...
        #Збереження даних існуючого клієнта
        self.declarant.save()

        updated_declarant = Declarant.objects.get(id=self.declarant.id)
        self.assertEqual(updated_declarant.surname, "Petrov")
        self.assertEqual(updated_declarant.name, "Vasil")
        #...

    def test_delete_declarant(self):
        declarant_id = self.declarant.id
        self.declarant.delete()
        #1
        with self.assertRaises(Declarant.DoesNotExist):
            Declarant.objects.get(id=declarant_id)