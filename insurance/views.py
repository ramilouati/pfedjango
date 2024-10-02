from rest_framework import viewsets
from .models import *
from .serializers import *

class AssureViewSet(viewsets.ModelViewSet):
    queryset = Assure.objects.all()
    serializer_class = AssureSerializer



# class EntretienViewSet(viewsets.ModelViewSet):
#     queryset = Entretien.objects.all()
#     serializer_class = EntretienSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ConstatViewSet(viewsets.ModelViewSet):
#     queryset = Constat.objects.all()
#     serializer_class = ConstatSerializer

# class DegatApparentViewSet(viewsets.ModelViewSet):
#     queryset = DegatApparent.objects.all()
#     serializer_class = DegatApparentSerializer

# class ConversationViewSet(viewsets.ModelViewSet):
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationSerializer
