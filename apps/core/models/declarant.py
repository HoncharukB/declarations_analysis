from django.db import models

class Declarant(models.Model):
    user_declarant_id = models.IntegerField(unique=True)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)

    work_place = models.CharField(max_length=255, null=True, blank=True)
    work_post = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    
# class Gender(models.IntegerChoices):
#     NOT_SPECIFIED = 0, "Not specified"
#     MALE = 1, "Male"
#     FEMALE = 2, "Female"
#     OTHER = 3, "Other"
#
# class Declarations(models.Model):
#     id = models.AutoField(primary_key=True)
#     surname = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     patronymic = models.CharField(max_length=50)
#     email = models.EmailField()
#     birthdate = models.DateField()
#     gender = models.IntegerField(choices=Gender.choices)