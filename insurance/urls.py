from django.urls import path, include
from rest_framework.routers import DefaultRouter
from insurance.views import AssureViewSet 

router = DefaultRouter()
router.register(r'assures', AssureViewSet)
# router.register(r'entretiens', EntretienViewSet)
# router.register(r'users', UserViewSet)
# router.register(r'constats', ConstatViewSet)
# router.register(r'degat-apparents', DegatApparentViewSet)
# router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('assures/', AssureViewSet.as_view({'get': 'list', 'post': 'create'}), name='assure-list'),
]


