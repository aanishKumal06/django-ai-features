from .views import health_advice_view, all_advice_view
from django.urls import path

urlpatterns = [
    path("advice/<int:patient_id>/", health_advice_view, name="health_advice"),
    path("advice/", all_advice_view, name="all_advice"),
]
