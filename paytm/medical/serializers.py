from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.fields import BooleanField

from medical.models import Patient, Prescription, MedicalRecord, ViewRequest, BaseUser, AbstractBusinessUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class ViewRequestSerializer2(serializers.ModelSerializer):

    class Meta:
        depth = 2
        model = ViewRequest
        fields = '__all__'

class ViewRequestSerializer(serializers.ModelSerializer):
    patient = PrimaryKeyRelatedField(required=False, queryset=Patient.objects)
    business_user = PrimaryKeyRelatedField(required=False, queryset=AbstractBusinessUser.objects)
    allowed = BooleanField(required=True)

    class Meta:
        depth = 2
        model = ViewRequest
        fields = ['patient', 'business_user', 'allowed']
