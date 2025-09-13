import unittest
import uuid

from apps.core.models.owner import OwnerType, Owner


class OwnerModelTest(unittest.TestCase):

    def setUp(self):
        self.owner_data_1 = {
            'owner_type': OwnerType.PERSON,
            'name': 'Vasyl Petrenko',
            'identifier': uuid.uuid4().hex,
        }
        self.owner_data_2 = {
            'owner_type': OwnerType.PERSON,
            'name': 'Ivan Novak',
            'identifier': uuid.uuid4().hex,
        }
        self.owner1 = Owner.objects.create(**self.owner_data_1)
        self.owner2 = Owner.objects.create(**self.owner_data_2)

    def test_create_owner(self):
        owner1 = Owner.objects.get(id=self.owner1.id)
        owner2 = Owner.objects.get(id=self.owner2.id)
        print(owner1)
        print(owner2)

        self.assertEqual(owner1.owner_type, self.owner_data_1['owner_type'])
        self.assertEqual(owner1.name, self.owner_data_1['name'])
        self.assertEqual(owner1.identifier, self.owner_data_1['identifier'])
        self.assertEqual(owner2.owner_type, self.owner_data_2['owner_type'])
        self.assertEqual(owner2.name, self.owner_data_2['name'])
        self.assertEqual(owner2.identifier, self.owner_data_2['identifier'])

    def test_update_owner(self):
        self.owner1.name = "Kolya Pupkin"
        self.owner1.save()
        updated_owner = Owner.objects.get(id=self.owner1.id)
        self.assertEqual(updated_owner.name, "Kolya Pupkin")

    def test_delete_owner(self):
        owner_id = self.owner2.id
        self.owner2.delete()
        with self.assertRaises(Owner.DoesNotExist):
            Owner.objects.get(id=owner_id)

    def tearDown(self):
        Owner.objects.all().delete()