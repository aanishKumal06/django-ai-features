from .views import doctor_list
from django.urls import path

urlpatterns = [
    path("", doctor_list, name="doctor_list"),
]
