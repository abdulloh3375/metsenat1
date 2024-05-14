from django.db import models
from datetime import datetime



class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)

    class Meta:
        abstract = True



class Sponsor(BaseModel):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    organization = models.CharField(max_length=50)
    
    class SponsorType(models.TextChoices):
       
        YURIDIC = 'yuridik', 'Yuridik'
        JISMONIY = 'jismoniy', 'Jismoniy'

    class Status(models.TextChoices):

        NEW = 'new', 'New'
        CONFIRM = 'confirm', 'Confirm'
        CENCELED = 'cenceled', 'Cenceled'
        MODERATION = 'moderation', 'Modiration'
    
    class Payment(models.TextChoices):
        CARD = 'Karta', 'Plastik karta'
        CASH = 'Naqd', 'Naqd'
    
    sponsor_type = models.CharField(max_length=100, choices=SponsorType.choices, null=True)
    status = models.CharField(max_length=50,choices=Status.choices, null=True)
    payment_type = models.CharField(max_length=50, choices=Payment.choices, null=True)

    def __str__(self) -> str:
        return self.full_name
    


class University(BaseModel):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title
    


class Student(BaseModel):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)

    class StudentType(models.TextChoices):

        BACHALAR = 'bachalar', 'Bachalar'
        MAGISTER = 'magister', 'Magister'

    student_type = models.CharField(max_length=50, choices=StudentType.choices, default=StudentType.BACHALAR)
    contract = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self) -> str:
        return self.full_name



class StudentSponsor(BaseModel):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT, related_name='student_sponsors', null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='student_sponsors', null=True)
