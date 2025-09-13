import unittest
import uuid
from decimal import Decimal
from datetime import date
from apps.core.models.realestate import RealEstate, RealEstateDeclaration
from apps.core.models import Declaration, Declarant, Owner
from apps.core.models.owner import OwnerType


class RealEstateModelTests(unittest.TestCase):
    id_counter = 50

    def setUp(self):
        RealEstateModelTests.id_counter += 1

        # Створюємо власників
        self.owner_data_1 = {
            'owner_type': OwnerType.PERSON,
            'name': 'Owner One',
            'identifier': uuid.uuid4().hex,
        }
        self.owner1 = Owner.objects.create(**self.owner_data_1)

        self.owner_data_2 = {
            'owner_type': OwnerType.PERSON,
            'name': 'Owner Two',
            'identifier': uuid.uuid4().hex,
        }
        self.owner2 = Owner.objects.create(**self.owner_data_2)

        # Створюємо декларанта
        self.declarant_data = {
            'user_declarant_id': RealEstateModelTests.id_counter,
            'api_id': uuid.uuid4(),
            'surname': 'Petrenko',
            'name': 'Vasyl',
            'patronymic': 'Ivanovich',
            'work_place': 'IT Step',
            'work_post': 'Developer',
            'owner': self.owner1,
        }
        self.declarant = Declarant.objects.create(**self.declarant_data)

        # Створюємо декларації
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
        self.declaration1 = Declaration.objects.create(**self.declaration_data_1)
        self.declaration2 = Declaration.objects.create(**self.declaration_data_2)

        # Створюємо обʼєкти RealEstate
        self.real_estate_data_1 = {
            'object_type': 'Apartment',
            'other_object_type': None,
            'region': 'Kyivska',
            'city': 'Kyiv',
            'total_area': Decimal('85.5'),
            'cost_date_assessment': Decimal('1200000'),
            'owning_date': date(2015, 5, 10),
            'reg_number': 'REG123',
            'object_cost_type': 'Market',
        }
        self.real_estate_data_2 = {
            'object_type': 'House',
            'other_object_type': 'Detached',
            'region': 'Lvivska',
            'city': 'Lviv',
            'total_area': Decimal('150.0'),
            'cost_date_assessment': Decimal('3500000'),
            'owning_date': date(2010, 9, 20),
            'reg_number': 'REG456',
            'object_cost_type': 'Market',
        }
        self.real_estate1 = RealEstate.objects.create(**self.real_estate_data_1)
        self.real_estate2 = RealEstate.objects.create(**self.real_estate_data_2)

        # Створюємо записи у проміжній таблиці RealEstateDeclaration з iteration
        RealEstateDeclaration.objects.create(
            real_estate=self.real_estate1,
            declaration=self.declaration1,
            iteration='iter1'
        )
        RealEstateDeclaration.objects.create(
            real_estate=self.real_estate1,
            declaration=self.declaration2,
            iteration='iter2'
        )
        RealEstateDeclaration.objects.create(
            real_estate=self.real_estate2,
            declaration=self.declaration2,
            iteration='iter3'
        )

        # Додаємо зв’язки ManyToMany на owners
        self.real_estate1.owners.add(self.owner1)
        self.real_estate2.owners.add(self.owner1, self.owner2)

    def test_create_real_estate_relations(self):
        re1 = RealEstate.objects.get(id=self.real_estate1.id)
        re2 = RealEstate.objects.get(id=self.real_estate2.id)
        print(re1)
        print(re2)

        self.assertEqual(re1.city, 'Kyiv')
        self.assertEqual(re2.city, 'Lviv')

        # Перевірка ManyToMany owners
        self.assertIn(self.owner1.id, re1.owners.values_list('id', flat=True))
        self.assertIn(self.owner2.id, re2.owners.values_list('id', flat=True))

        # Перевірка декларацій через проміжну модель
        decl_ids_re1 = set(re1.declarations.values_list('id', flat=True))
        self.assertIn(self.declaration1.id, decl_ids_re1)
        self.assertIn(self.declaration2.id, decl_ids_re1)

        decl_ids_re2 = set(re2.declarations.values_list('id', flat=True))
        self.assertIn(self.declaration2.id, decl_ids_re2)

    def test_update_real_estate(self):
        self.real_estate1.city = 'Odesa'
        self.real_estate1.save()
        updated = RealEstate.objects.get(id=self.real_estate1.id)
        self.assertEqual(updated.city, 'Odesa')

    def test_delete_real_estate(self):
        re2_id = self.real_estate2.id
        self.real_estate2.delete()
        with self.assertRaises(RealEstate.DoesNotExist):
            RealEstate.objects.get(id=re2_id)

    def tearDown(self):
        RealEstateDeclaration.objects.all().delete()
        RealEstate.objects.all().delete()
        Declaration.objects.all().delete()
        Declarant.objects.all().delete()
        Owner.objects.all().delete()
