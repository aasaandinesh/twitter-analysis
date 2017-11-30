from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import mixins, generics

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from medical.models import Patient, Prescription, MedicalRecord, AbstractBusinessUser, ViewRequest, BaseUser, \
    AbstractUser
from medical.serializers import PatientSerializer, PrescriptionSerializer, MedicalRecordSerializer, BaseUserSerializer, \
    ViewRequestSerializer, ViewRequestSerializer2
import json

@csrf_exempt
def get_user_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        user = BaseUser.objects.get(username=username)
        serializer = BaseUserSerializer(user)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def patients_list(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return JsonResponse(serializer.data, safe=False)


class PrescriptionAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def get(self, request, *args, **kwargs):
        patient_id = request.GET.get('patient_id')
        buser_id = request.GET.get('buser_id')
        if buser_id is None:
            self.queryset = Prescription.objects.filter(medicalrecord__patient__id=patient_id)
            return self.list(request, *args, **kwargs)
        else:
            r = ViewRequest.objects.get(patient__id=patient_id, business_user__id=buser_id)
            if r.allowed:
                self.queryset = Prescription.objects.filter(medicalrecord__patient__id=patient_id)
                return self.list(request, *args, **kwargs)


class MedicalRecordAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get(self, request, *args, **kwargs):
        patient_id = request.GET.get('patient_id')
        buser_id = request.GET.get('buser_id')
        if buser_id is None:
            self.queryset = MedicalRecord.objects.filter(patient__id=patient_id)
            return self.list(request, *args, **kwargs)
        else:
            r = ViewRequest.objects.get(patient__id=patient_id, business_user__id=buser_id)
            if r.allowed:
                self.queryset = Prescription.objects.filter(patient__id=patient_id)
                return self.list(request, *args, **kwargs)


class ViewRequestAPIView(mixins.ListModelMixin, generics.GenericAPIView, mixins.UpdateModelMixin,
                         mixins.CreateModelMixin):
    queryset = ViewRequest.objects.all()
    serializer_class = ViewRequestSerializer2

    def get(self, request, *args, **kwargs):
        patient_id = request.GET.get('patient_id')
        buser_id = request.GET.get('buser_id')
        if patient_id is not None:
            self.queryset = ViewRequest.objects.filter(patient_id=patient_id)
            return self.list(request, *args, **kwargs)

        if buser_id is not None:
            self.queryset = ViewRequest.objects.filter(business_user__id=buser_id)
            return self.list(request, *args, **kwargs)

        if buser_id is not None and patient_id is not None:
            self.queryset = ViewRequest.objects.filter(business_user__id=buser_id, patient__id=patient_id)
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ViewRequestDetailAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = ViewRequest.objects.all()
    serializer_class = ViewRequestSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)






