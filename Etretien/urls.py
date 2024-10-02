from django.urls import path
from .views import EntretienViewSet

urlpatterns = [
    path('entretien/', EntretienViewSet.as_view(), name='entretien-list'),
]
