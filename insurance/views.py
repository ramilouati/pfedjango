from rest_framework import viewsets
from .models import *
from .serializers import *

class AssuranceContratViewSet(viewsets.ModelViewSet):
    queryset = AssuranceContrat.objects.all()
    serializer_class = AssuranceContratSerializer

class AssureViewSet(viewsets.ModelViewSet):
    queryset = Assure.objects.all()
    serializer_class = AssureSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class EntretienViewSet(viewsets.ModelViewSet):
    queryset = Entretien.objects.all()
    serializer_class = EntretienSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ConstatViewSet(viewsets.ModelViewSet):
    queryset = Constat.objects.all()
    serializer_class = ConstatSerializer

class DegatApparentViewSet(viewsets.ModelViewSet):
    queryset = DegatApparent.objects.all()
    serializer_class = DegatApparentSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
