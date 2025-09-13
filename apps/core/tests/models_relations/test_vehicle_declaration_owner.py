import unittest
import uuid
from datetime import date
from decimal import Decimal
from apps.core.models import Vehicle, Declaration, Declarant, Owner
from apps.core.models.owner import OwnerType

class VehicleModelTests(unittest.TestCase):
    id_counter = 50

    def setUp(self):
        VehicleModelTests.id_counter += 1

        self.owner1_data = {
            'owner_type': OwnerType.PERSON,
            'name': 'Owner One',
            'identifier': uuid.uuid4().hex,
        }
        self.owner1 = Owner.objects.create(**self.owner1_data)

        self.owner2_data = {
            'owner_type': OwnerType.PERSON,
            'name': 'Owner Two',
            'identifier': uuid.uuid4().hex,
        }
        self.owner2 = Owner.objects.create(**self.owner2_data)

        self.declarant_data = {
            'user_declarant_id': VehicleModelTests.id_counter,
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

        self.vehicle_data_1 = {
            'object_type': 'Car',
            'brand': 'Toyota',
            'model': 'Camry',
            'cost': Decimal('15000.00'),
            'owning_date': date(2018, 5, 20),
            'graduation_year': 2017,
        }
        self.vehicle_data_2 = {
            'object_type': 'Motorcycle',
            'brand': 'Honda',
            'model': 'CBR500R',
            'cost': Decimal('7000.00'),
            'owning_date': date(2020, 7, 10),
            'graduation_year': 2019,
        }

        self.vehicle1 = Vehicle.objects.create(**self.vehicle_data_1)
        self.vehicle2 = Vehicle.objects.create(**self.vehicle_data_2)

        self.vehicle1.declarations.add(self.declaration_1, self.declaration_2)
        self.vehicle1.owners.add(self.owner1)

        self.vehicle2.declarations.add(self.declaration_2)
        self.vehicle2.owners.add(self.owner1, self.owner2)

    def test_create_vehicle_relations(self):
        v1 = Vehicle.objects.get(id=self.vehicle1.id)
        v2 = Vehicle.objects.get(id=self.vehicle2.id)
        print(v1)
        print(v2)

        self.assertEqual(v1.brand, 'Toyota')
        self.assertEqual(v1.model, 'Camry')
        self.assertIn(self.declaration_1.id, v1.declarations.values_list('id', flat=True))
        self.assertIn(self.owner1.id, v1.owners.values_list('id', flat=True))

        self.assertEqual(v2.brand, 'Honda')
        self.assertEqual(v2.model, 'CBR500R')
        self.assertIn(self.declaration_2.id, v2.declarations.values_list('id', flat=True))
        self.assertIn(self.owner2.id, v2.owners.values_list('id', flat=True))

    def test_update_vehicle(self):
        self.vehicle1.cost = Decimal('16000.00')
        self.vehicle1.save()
        updated = Vehicle.objects.get(id=self.vehicle1.id)
        self.assertEqual(updated.cost, Decimal('16000.00'))

    def test_delete_vehicle(self):
        v2_id = self.vehicle2.id
        self.vehicle2.delete()
        with self.assertRaises(Vehicle.DoesNotExist):
            Vehicle.objects.get(id=v2_id)

    def tearDown(self):
        Vehicle.objects.all().delete()
        Declaration.objects.all().delete()
        Declarant.objects.all().delete()
        Owner.objects.all().delete()
