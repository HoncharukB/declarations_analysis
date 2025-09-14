import unittest
import uuid

from apps.core.models.owner import OwnerType, CitizenType, Owner


class OwnerModelTest(unittest.TestCase):

    def setUp(self):
        self.owner_data_1 = {
            'owner_type': OwnerType.PERSON,
            'first_name': 'Vasyl',
            'last_name': 'Petrenko',
            'identifier': uuid.uuid4().hex,
            'citizen': CitizenType.UKRAINIAN_CITIZEN,
        }
        self.owner_data_2 = {
            'owner_type': OwnerType.PERSON,
            'first_name': 'Ivan',
            'last_name': 'Novak',
            'identifier': uuid.uuid4().hex,
            'citizen': CitizenType.FOREIGN_CITIZEN,
        }
        self.owner1 = Owner.objects.create(**self.owner_data_1)
        self.owner2 = Owner.objects.create(**self.owner_data_2)

    def test_create_owner(self):
        owner1 = Owner.objects.get(id=self.owner1.id)
        owner2 = Owner.objects.get(id=self.owner2.id)
        print(owner1)
        print(owner2)

        self.assertEqual(owner1.owner_type, self.owner_data_1['owner_type'])
        self.assertEqual(owner1.first_name, self.owner_data_1['first_name'])
        self.assertEqual(owner1.last_name, self.owner_data_1['last_name'])
        self.assertEqual(owner1.identifier, self.owner_data_1['identifier'])
        self.assertEqual(owner1.citizen, self.owner_data_1['citizen'])

        self.assertEqual(owner2.owner_type, self.owner_data_2['owner_type'])
        self.assertEqual(owner2.first_name, self.owner_data_2['first_name'])
        self.assertEqual(owner2.last_name, self.owner_data_2['last_name'])
        self.assertEqual(owner2.identifier, self.owner_data_2['identifier'])
        self.assertEqual(owner2.citizen, self.owner_data_2['citizen'])

    def test_update_owner(self):
        self.owner1.first_name = "Kolya"
        self.owner1.last_name = "Pupkin"
        self.owner1.save()
        updated_owner = Owner.objects.get(id=self.owner1.id)
        self.assertEqual(updated_owner.first_name, "Kolya")
        self.assertEqual(updated_owner.last_name, "Pupkin")

    def test_delete_owner(self):
        owner_id = self.owner2.id
        self.owner2.delete()
        with self.assertRaises(Owner.DoesNotExist):
            Owner.objects.get(id=owner_id)

    def tearDown(self):
        Owner.objects.all().delete()