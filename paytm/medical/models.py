from django.db import models


# Create your models here.

class BaseModel(models.Model):
    pass


class AbstractUser(BaseModel):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)


class BaseUser(AbstractUser):
    user_type = models.CharField(max_length=2)


class Patient(BaseUser):
    pass


class AbstractBusinessUser(BaseUser):
    pass


class Doctor(AbstractBusinessUser):
    pass


class Pharmacist(AbstractBusinessUser):
    pass


class Prescription(BaseModel):
    details = models.CharField(max_length=500)


class MedicalRecord(BaseModel):
    doctor = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    prescription_details = models.CharField(max_length=1000)
    patient = models.ForeignKey(Patient, related_name="medical_records")


class ViewRequest(BaseModel):
    patient = models.ForeignKey(Patient)
    business_user = models.ForeignKey(AbstractBusinessUser)
    allowed = models.BooleanField(default=False)
