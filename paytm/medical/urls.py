"""paytm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from medical.views import patients_list, PrescriptionAPIView, get_user_data, MedicalRecordAPIView, ViewRequestAPIView, \
    ViewRequestDetailAPIView

urlpatterns = [
    url(r'^patients/$', patients_list, name='patient_list'),
    url(r'^prescription/$', PrescriptionAPIView.as_view(), name='prescription'),
    url(r'^medical_record/$', MedicalRecordAPIView.as_view(), name='medical_record'),
    url(r'^login/$', get_user_data, name='get_user_data'),
    url(r'^request/$', ViewRequestAPIView.as_view(), name='view_request'),
    url(r'^request/(?P<pk>[0-9]+)/$', ViewRequestDetailAPIView.as_view(), name='view_request_detail'),

    ]


