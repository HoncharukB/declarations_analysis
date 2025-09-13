import datetime
import unittest
import uuid
from apps.core.models import Declaration, Declarant
from apps.core.models.owner import Owner, OwnerType

class DeclarationModelTests(unittest.TestCase):
    id_counter = 50
    def setUp(self):
        DeclarationModelTests.id_counter += 1
        # Спершу створення Owner - необхідний для Declarant
        self.owner_data = {
            'owner_type': OwnerType.DECLARANT,
            'name': 'Vasyl Petrenko',
            'identifier': uuid.uuid4().hex,
        }
        self.owner = Owner.objects.create(**self.owner_data)

        # Створення Declarant
        self.declarant_data = {
            'user_declarant_id': DeclarationModelTests.id_counter,
            'api_id': uuid.uuid4(),
            'surname': 'Petrenko',
            'name': 'Vasyl',
            'patronymic': 'Ivanovich',
            'work_place': 'IT Step',
            'work_post': 'Developer',
            'owner': self.owner,
        }
        # Створення об'єкту, запис об'єкта в таблицю бази даних, присвоєння id об'єкту
        self.declarant = Declarant.objects.create(**self.declarant_data)

        # Створення двох декларацій для одного декларанта
        self.declaration_data_1 = {
            'document_id': uuid.uuid4(),
            'declaration_year': 2023,
            'declaration_type': 1,
            'date': datetime.date.today(),
            'declarant': self.declarant,
        }
        self.declaration_data_2 = {
            'document_id': uuid.uuid4(),
            'declaration_year': 2024,
            'declaration_type': 2,
            'date': datetime.date.today(),
            'declarant': self.declarant,
        }

        self.declaration_1 = Declaration.objects.create(**self.declaration_data_1)
        self.declaration_2 = Declaration.objects.create(**self.declaration_data_2)

    def test_create_declarations(self):
        decl_1 = Declaration.objects.get(id=self.declaration_1.id)
        decl_2 = Declaration.objects.get(id=self.declaration_2.id)
        print(decl_1)
        print(decl_2)
        self.assertEqual(decl_1.declarant.id, self.declarant.id)
        self.assertEqual(decl_1.declaration_year, 2023)
        self.assertEqual(decl_2.declaration_type, 2)

    def test_update_declaration(self):
        self.declaration_1.declaration_year = 2025
        self.declaration_1.save()
        updated = Declaration.objects.get(id=self.declaration_1.id)
        self.assertEqual(updated.declaration_year, 2025)

    def test_delete_declaration(self):
        decl_id = self.declaration_2.id
        self.declaration_2.delete()
        with self.assertRaises(Declaration.DoesNotExist):
            Declaration.objects.get(id=decl_id)

    def tearDown(self):
        Declaration.objects.all().delete()
        Declarant.objects.all().delete()
        Owner.objects.all().delete()
