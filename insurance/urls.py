from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'assures', AssureViewSet)
router.register(r'assurance-contrats', AssuranceContratViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'entretiens', EntretienViewSet)
router.register(r'users', UserViewSet)
router.register(r'constats', ConstatViewSet)
router.register(r'degat-apparents', DegatApparentViewSet)
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('api', include(router.urls)),
]


