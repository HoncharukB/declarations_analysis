import random
import unittest
import uuid
from datetime import date
from apps.core.models import BankAccount, Declaration, Declarant, Owner
from apps.core.models.owner import OwnerType, CitizenType

class BankAccountModelTests(unittest.TestCase):
    def setUp(self):
        user_declarant_id = random.randint(1, 2 ** 63 - 1)
        self.owner1_data = {
            'owner_type': OwnerType.PERSON,
            'first_name': 'Owner',
            'last_name': 'One',
            'identifier': uuid.uuid4().hex,
            'citizen': CitizenType.UKRAINIAN_CITIZEN,
        }
        self.owner1 = Owner.objects.create(**self.owner1_data)

        self.owner2_data = {
            'owner_type': OwnerType.PERSON,
            'first_name': 'Owner',
            'last_name': 'Two',
            'identifier': uuid.uuid4().hex,
            'citizen': CitizenType.UKRAINIAN_CITIZEN,
        }
        self.owner2 = Owner.objects.create(**self.owner2_data)

        self.declarant_data = {
            'user_declarant_id': user_declarant_id,
            'api_id': uuid.uuid4(),
            'lastname': 'Petrenko',
            'firstname': 'Vasyl',
            'middlename': 'Ivanovich',
            'work_place': 'IT Step',
            'work_post': 'Developer',
            'actual_country': 1,
            'owner': self.owner1,
        }
        self.declarant = Declarant.objects.create(**self.declarant_data)

        self.declaration_data_1 = {
            'document_id': uuid.uuid4(),
            'document_type': 1,
            'declaration_year': 2023,
            'declaration_type': 1,
            'date': date.today(),
            'declarant': self.declarant,
        }
        self.declaration_data_2 = {
            'document_id': uuid.uuid4(),
            'document_type': 1,
            'declaration_year': 2024,
            'declaration_type': 2,
            'date': date.today(),
            'declarant': self.declarant,
        }
        self.declaration_1 = Declaration.objects.create(**self.declaration_data_1)
        self.declaration_2 = Declaration.objects.create(**self.declaration_data_2)

        self.bank_account_data_1 = {
            'object_type': 'Кошти, розміщені на банківських рахунках',
            'currency': 'USD',
            'amount': 8654,
            'organization': 'Bank Handlowy w Warszawie S.A.',
            'organization_type': 'Юридична особа, зареєстрована в Україні',
            'organization_ua_company_code': '14360570',
            'iteration': '12345',
            'extra_info': {'notes': 'Some extra info'},
        }
        self.bank_account_data_2 = {
            'object_type': 'Кошти, розміщені на банківських рахунках',
            'currency': 'EUR',
            'amount': 6800,
            'organization': '[Конфіденційна інформація]',
            'organization_type': 'Юридична особа, зареєстрована в Україні',
            'organization_ua_company_code': '21111111',
            'iteration': '67890',
            'extra_info': {'notes': 'Other info'},
        }
        self.bank_account1 = BankAccount.objects.create(**self.bank_account_data_1)
        self.bank_account2 = BankAccount.objects.create(**self.bank_account_data_2)

        self.bank_account1.declarations.add(self.declaration_1, self.declaration_2)
        self.bank_account1.owners.add(self.owner1)

        self.bank_account2.declarations.add(self.declaration_2)
        self.bank_account2.owners.add(self.owner1, self.owner2)

    def test_create_bank_account_relations(self):
        ba1 = BankAccount.objects.get(id=self.bank_account1.id)
        ba2 = BankAccount.objects.get(id=self.bank_account2.id)
        print(ba1)
        print(ba2)

        self.assertEqual(ba1.amount, 8654)
        self.assertIn(self.declaration_1.id, ba1.declarations.values_list('id', flat=True))
        self.assertIn(self.owner1.id, ba1.owners.values_list('id', flat=True))

        self.assertEqual(ba2.amount, 6800)
        self.assertIsNone(ba2.organization)  # Перевірка, що конфіденційна інформація очищена
        self.assertIn(self.declaration_2.id, ba2.declarations.values_list('id', flat=True))
        self.assertIn(self.owner2.id, ba2.owners.values_list('id', flat=True))

    def test_update_bank_account(self):
        self.bank_account1.amount = 12000
        self.bank_account1.save()
        updated_ba1 = BankAccount.objects.get(id=self.bank_account1.id)
        self.assertEqual(updated_ba1.amount, 12000)

    def test_delete_bank_account(self):
        ba2_id = self.bank_account2.id
        self.bank_account2.delete()
        with self.assertRaises(BankAccount.DoesNotExist):
            BankAccount.objects.get(id=ba2_id)

    def tearDown(self):
        BankAccount.objects.all().delete()
        Declaration.objects.all().delete()
        Declarant.objects.all().delete()
        Owner.objects.all().delete()