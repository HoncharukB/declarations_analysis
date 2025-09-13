import unittest
import uuid
from datetime import date
from apps.core.models import FamilyMember, Declaration, Declarant, Owner
from apps.core.models.owner import OwnerType

class FamilyMemberModelTests(unittest.TestCase):
    id_counter = 50

    def setUp(self):
        FamilyMemberModelTests.id_counter += 1

        # Створюємо власника з типом family
        self.owner_data = {
            'owner_type': OwnerType.FAMILY,
            'name': 'Family Member Owner',
            'identifier': uuid.uuid4().hex,
        }
        self.owner = Owner.objects.create(**self.owner_data)

        # Створюємо декларанта
        self.declarant_data = {
            'user_declarant_id': FamilyMemberModelTests.id_counter,
            'api_id': uuid.uuid4(),
            'surname': 'Petrenko',
            'name': 'Vasyl',
            'patronymic': 'Ivanovich',
            'work_place': 'IT Step',
            'work_post': 'Developer',
            'owner': self.owner,
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
        self.declaration_1 = Declaration.objects.create(**self.declaration_data_1)
        self.declaration_2 = Declaration.objects.create(**self.declaration_data_2)

        # Створюємо FamilyMember з посиланням на owner та declarations
        self.family_member_data = {
            'api_id' : uuid.uuid4(),
            'relation_type' : 'sibling',
            'surname' : 'Ivanov',
            'name' : 'Ivan',
            'patronymic' : 'Ivanovich',
            'owner' : self.owner,
        }
        self.family_member = FamilyMember.objects.create(**self.family_member_data)

        self.family_member.declarations.add(self.declaration_1, self.declaration_2)

    def test_create_family_member(self):
        fm = FamilyMember.objects.get(id=self.family_member.id)
        print(fm)
        self.assertEqual(fm.surname, 'Ivanov')
        self.assertEqual(fm.owner.id, self.owner.id)
        decl_ids = set(fm.declarations.values_list('id', flat=True))
        self.assertIn(self.declaration_1.id, decl_ids)
        self.assertIn(self.declaration_2.id, decl_ids)

    def test_update_family_member(self):
        self.family_member.name = 'Petro'
        self.family_member.save()
        updated = FamilyMember.objects.get(id=self.family_member.id)
        self.assertEqual(updated.name, 'Petro')

    def test_delete_family_member(self):
        fm_id = self.family_member.id
        self.family_member.delete()
        with self.assertRaises(FamilyMember.DoesNotExist):
            FamilyMember.objects.get(id=fm_id)

    def tearDown(self):
        FamilyMember.objects.all().delete()
        Declaration.objects.all().delete()
        Declarant.objects.all().delete()
        Owner.objects.all().delete()