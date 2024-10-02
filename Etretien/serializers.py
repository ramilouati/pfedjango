from insurance.models import Assure
from rest_framework import serializers
from Etretien.models import Entretien

class EntretiensSerializer(serializers.ModelSerializer):
    # Use AssureSerializer as a nested serializer for create and update
    # assure = serializers.SerializerMethodField()

    class Meta:
        model = Entretien
        fields = ['id', 'nom_entretien', 'kilometrage', 'date', 'vehicle']
    def create(self, validated_data):
        # Fetch the latest Assure instance
        # assure = Assure.objects.latest('id')  # Adjust field as needed to fetch the latest record

        # Create the Vehicle instance with the latest Assure
        entretien = Entretien.objects.create( **validated_data)
        return entretien
    

    # def update(self, instance, validated_data):
    #     # Extract assure data from validated_data
    #     assure_data = validated_data.pop('assure', None)

    #     # if assure_data:
    #     #     # Update the nested Assure data
    #     #     assure_serializer = AssureSerializer(instance.assure, data=assure_data)
    #     #     assure_serializer.is_valid(raise_exception=True)
    #     #     assure_serializer.save()

    #     # Update the vehicle fields
    #     instance.marque = validated_data.get('marque', instance.marque)
    #     instance.type = validated_data.get('type', instance.type)
    #     instance.model = validated_data.get('model', instance.model)
    #     instance.date_fabrication = validated_data.get('date_fabrication', instance.date_fabrication)
    #     instance.save()

    #     return instance
