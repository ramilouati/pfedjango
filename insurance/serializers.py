from insurance.models import Assure
from rest_framework import serializers

class AssureSerializer(serializers.ModelSerializer):
    # Assuming you want to serialize vehicles along with assure, but vehicles is optional
    vehicles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # or you can define a custom method

    class Meta:
        model = Assure
        fields = ['nom', 'prenom', 'adresse', 'tel', 'nom_assurance', 'police', 'agence', 'date_debut_attestation', 'date_fin_attestation', 'vehicles']

    # Optionally, you can define a method to return serialized vehicles data if needed
    def get_vehicles(self, obj):
        from Vehicles.serializers import VehicleSerializer  # Import locally to avoid circular import
        vehicles = obj.vehicles.all()
        return VehicleSerializer(vehicles, many=True).data


    def create(self, validated_data):
        # Handle vehicles data if it exists

        # Create the Assure instance
        assure = Assure.objects.create(**validated_data)

        # If vehicles data is provided, create vehicle entries linked to assure

        return assure

    def update(self, instance, validated_data):
        # Pop the vehicles data if it exists
        vehicles_data = validated_data.pop('vehicles', None)

        # Update the Assure instance
        instance.nom = validated_data.get('nom', instance.nom)
        instance.prenom = validated_data.get('prenom', instance.prenom)
        instance.address = validated_data.get('address', instance.address)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.nom_assurance = validated_data.get('nom_assurance', instance.nom_assurance)
        instance.police = validated_data.get('police', instance.police)
        instance.agence = validated_data.get('agence', instance.agence)
        instance.date_debut_attestation = validated_data.get('date_debut_attestation', instance.date_debut_attestation)
        instance.date_fin_attestation = validated_data.get('date_fin_attestation', instance.date_fin_attestation)
        instance.save()

        # If vehicles data is provided, update or create vehicle entries linked to assure
        if vehicles_data:
            for vehicle_data in vehicles_data:
                # You can update existing vehicles or create new ones as needed
                Vehicle.objects.update_or_create(assure=instance, **vehicle_data)

        return instance


# class EntretienSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Entretien
#         fields = '__all__'
# class ConstatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Constat
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


# class AssuranceContratSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AssuranceContrat
#         fields = ['id', 'nom_assurance', 'police', 'agence', 'date_debut_attestation', 'date_fin_attestation']

# class DegatApparentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DegatApparent
#         fields = '__all__'

# class ConversationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Conversation
#         fields = '__all__'
