import random
import unittest
import uuid
from decimal import Decimal
from datetime import date
from apps.core.models import Income, Declaration, Declarant, Owner
from apps.core.models.owner import OwnerType

class IncomeModelTests(unittest.TestCase):
    def setUp(self):
        user_declarant_id = random.randint(1, 2 ** 63 - 1)
        # Створюємо Owners
        self.owner_data_1 = {
            'owner_type': OwnerType.PERSON,
            'first_name': 'Owner',
            'last_name': 'One',
            'identifier': uuid.uuid4().hex,
        }
        self.owner1 = Owner.objects.create(**self.owner_data_1)

        self.owner_data_2 = {
            'owner_type': OwnerType.PERSON,
            'first_name': 'Owner',
            'last_name': 'Two',
            'identifier': uuid.uuid4().hex,
        }
        self.owner2 = Owner.objects.create(**self.owner_data_2)

        # Створюємо Declarant і декларації
        self.declarant_data = {
            'user_declarant_id': user_declarant_id,
            'api_id': uuid.uuid4(),
            'surname': 'Petrenko',
            'name': 'Vasyl',
            'patronymic': 'Ivanovich',
            'work_place': 'IT Step',
            'work_post': 'Developer',
            'owner': self.owner1,
        }
        self.declarant = Declarant.objects.create(**self.declarant_data)

        self.declaration_data_1 = {
            'document_id': uuid.uuid4(),
            'declaration_year': 2023,
            'declaration_type': 1,
            'date': date.today(),
            'declarant': self.declarant,
        }
        self.declaration_data_2 = {
            'document_id': uuid.uuid4(),
            'declaration_year': 2024,
            'declaration_type': 2,
            'date': date.today(),
            'declarant': self.declarant,
        }

        self.declaration_1 = Declaration.objects.create(**self.declaration_data_1)
        self.declaration_2 = Declaration.objects.create(**self.declaration_data_2)

        # Створюємо Income
        self.income_data_1 = {
            'object_type': 'Salary',
            'amount': Decimal('5500.00'),
            'source_ua_company_name' : 'IT Company',
            'income_source' : 'j',
            'source_citizen' : 'Юридична особа, зареєстрована в Україні',
            'source_ua_company_code' : '123456',
            'iteration' : '12345',
            'extra_info' : {'notes': 'Important client'},
        }
        self.income_data_2 = {
            'object_type': 'Bonus',
            'amount': Decimal('4500.00'),
            'source_ua_company_name' : '[Конфіденційна інформація]',
            'income_source' : 'k',
            'source_citizen' : 'Фізична особа',
            'source_ua_company_code' : '654321',
            'iteration' : '67890',
            'extra_info' : {'notes': 'Secret bonus'},
        }

        self.income1 = Income.objects.create(**self.income_data_1)
        self.income2 = Income.objects.create(**self.income_data_2)

        # Прив’язуємо incomes до декларацій та овнерів
        self.income1.declarations.add(self.declaration_1, self.declaration_2)
        self.income1.owners.add(self.owner1)
        self.income2.declarations.add(self.declaration_2)
        self.income2.owners.add(self.owner1, self.owner2)

    def test_create_income_relations(self):
        income1 = Income.objects.get(id=self.income1.id)
        income2 = Income.objects.get(id=self.income2.id)
        print(income1)
        print(income2)
        self.assertEqual(income1.amount, Decimal('5500.00'))
        self.assertIn(self.declaration_1.id, income1.declarations.values_list('id', flat=True))
        self.assertIn(self.owner1.id, income1.owners.values_list('id', flat=True))
        self.assertIn(self.declaration_2.id, income2.declarations.values_list('id', flat=True))
        self.assertIn(self.owner2.id, income2.owners.values_list('id', flat=True))
        # Перевірка очистки конфіденційної інформації
        self.assertIsNone(income2.source_ua_company_name)

    def test_update_income(self):
        self.income1.object_type = 'Consulting'
        self.income1.amount = Decimal('2000.00')
        self.income1.save()
        updated_income = Income.objects.get(id=self.income1.id)
        self.assertEqual(updated_income.object_type, 'Consulting')
        self.assertEqual(updated_income.amount, Decimal('2000.00'))

    def test_delete_income(self):
        income_id = self.income2.id
        self.income2.delete()
        with self.assertRaises(Income.DoesNotExist):
            Income.objects.get(id=income_id)

    def tearDown(self):
        Income.objects.all().delete()
        Declaration.objects.all().delete()
        Declarant.objects.all().delete()
        Owner.objects.all().delete()