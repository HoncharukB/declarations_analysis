import random
import unittest
import uuid
from apps.core.models import Declarant, Owner
from apps.core.models.owner import OwnerType, CitizenType


# Test Case - Набір тестів
class DeclarantModelTest(unittest.TestCase):
    # Pre Condition Запускається перед кожним тестом
    # Створення тестового клієнта перед кожним тестом
    def setUp(self):
        user_declarant_id = random.randint(1, 2 ** 63 - 1)
        self.owner_data = {
            'owner_type': OwnerType.DECLARANT,
            'first_name': 'Vasyl',
            'last_name': 'Petrenko',
            'identifier': uuid.uuid4().hex,
            'citizen': CitizenType.UKRAINIAN_CITIZEN,
        }
        self.owner = Owner.objects.create(**self.owner_data)

        self.declarant_data = {
            'user_declarant_id': user_declarant_id,
            'api_id': uuid.uuid4(),
            'lastname': 'Petrenko',
            'firstname': 'Vasyl',
            'middlename': 'Ivanovich',
            'work_place': 'IT Step',
            'work_post': 'Developer',
            'actual_country': 1,
            'owner': self.owner,
        }
        # Створення об'єкту, запис об'єкта в таблицю бази даних, присвоєння id об'єкту
        self.declarant = Declarant.objects.create(**self.declarant_data)

    # Test - Метод - Окремий тест
    # Перевірка чи вірно створився декларант в таблиці
    def test_create_declarant(self):
        declarant = Declarant.objects.get(id=self.declarant.id)
        print(declarant)
        # Перевірка даних
        self.assertEqual(declarant.lastname, self.declarant_data['lastname'])
        self.assertEqual(declarant.owner.id, self.owner.id)
        self.assertEqual(declarant.firstname, self.declarant_data['firstname'])
        self.assertEqual(declarant.middlename, self.declarant_data['middlename'])
        self.assertEqual(declarant.work_place, self.declarant_data['work_place'])
        self.assertEqual(declarant.work_post, self.declarant_data['work_post'])

    def test_update_declarant(self):
        self.declarant.lastname = "Ivanenko"
        self.declarant.firstname = "Petro"
        #...
        #Збереження даних існуючого клієнта
        self.declarant.save()

        updated_declarant = Declarant.objects.get(id=self.declarant.id)
        self.assertEqual(updated_declarant.lastname, "Ivanenko")
        self.assertEqual(updated_declarant.firstname, "Petro")
        #...

    def test_delete_declarant(self):
        declarant_id = self.declarant.id
        self.declarant.delete()
        #1
        with self.assertRaises(Declarant.DoesNotExist):
            Declarant.objects.get(id=declarant_id)

        # Post Condition - Запускається після кожного методу класу
    def tearDown(self):
        # Видалення всіх записів із таблиці бази даних після виконання кожного тесту
        Declarant.objects.all().delete()
        Owner.objects.all().delete()