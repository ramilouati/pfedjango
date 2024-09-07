from rest_framework import serializers
from .models import *


class AssuranceContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssuranceContrat
        fields = '__all__'


class AssureSerializer(serializers.ModelSerializer):
    contrat = AssuranceContratSerializer()  # Nested serializer to include AssuranceContrat details

    class Meta:
        model = Assure
        fields = ['id', 'nom', 'prenom', 'adresse', 'tel', 'contrat']

    # Optional: Create or update related AssuranceContrat data
    def create(self, validated_data):
        contrat_data = validated_data.pop('contrat')
        contrat = AssuranceContrat.objects.create(**contrat_data)
        assure = Assure.objects.create(contrat=contrat, **validated_data)
        return assure

    def update(self, instance, validated_data):
        contrat_data = validated_data.pop('contrat')
        instance.nom = validated_data.get('nom', instance.nom)
        instance.prenom = validated_data.get('prenom', instance.prenom)
        instance.adresse = validated_data.get('adresse', instance.adresse)
        instance.tel = validated_data.get('tel', instance.tel)

        # Update or create AssuranceContrat
        contrat = instance.contrat
        contrat.nom_assurance = contrat_data.get('nom_assurance', contrat.nom_assurance)
        contrat.police = contrat_data.get('police', contrat.police)
        contrat.agence = contrat_data.get('agence', contrat.agence)
        contrat.date_debut_attestation = contrat_data.get('date_debut_attestation', contrat.date_debut_attestation)
        contrat.date_fin_attestation = contrat_data.get('date_fin_attestation', contrat.date_fin_attestation)
        contrat.save()

        instance.save()
        return instance

    def create(self, validated_data):
        # Pop nested data for contrat and vehicles
        contrat_data = validated_data.pop('contrat')
        vehicles_data = validated_data.pop('vehicles')

        # Create AssuranceContrat object
        contrat = AssuranceContrat.objects.create(**contrat_data)

        # Create Assure object
        assure = Assure.objects.create(contrat=contrat, **validated_data)

        # Create associated Vehicle objects
        for vehicle_data in vehicles_data:
            Vehicle.objects.create(assure=assure, **vehicle_data)

        return assure

class VehicleSerializer(serializers.ModelSerializer):
    assure = AssureSerializer()  # Nested serializer to include Assure details

    class Meta:
        model = Vehicle
        fields = ['id', 'marque', 'type', 'model', 'date_fabrication', 'assure']

    def create(self, validated_data):
        assure_data = validated_data.pop('assure')
        assure_serializer = AssureSerializer(data=assure_data)
        if assure_serializer.is_valid():
            assure = assure_serializer.save()
        vehicle = Vehicle.objects.create(assure=assure, **validated_data)
        return vehicle

    def update(self, instance, validated_data):
        assure_data = validated_data.pop('assure')
        assure_serializer = AssureSerializer(instance.assure, data=assure_data)
        if assure_serializer.is_valid():
            assure_serializer.save()

        instance.marque = validated_data.get('marque', instance.marque)
        instance.type = validated_data.get('type', instance.type)
        instance.model = validated_data.get('model', instance.model)
        instance.date_fabrication = validated_data.get('date_fabrication', instance.date_fabrication)
        instance.save()
        return instance



class EntretienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entretien
        fields = '__all__'
class ConstatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constat
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AssuranceContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssuranceContrat
        fields = ['id', 'nom_assurance', 'police', 'agence', 'date_debut_attestation', 'date_fin_attestation']

class DegatApparentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DegatApparent
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
