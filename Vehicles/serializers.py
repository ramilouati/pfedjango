from insurance.serializers import AssureSerializer
from rest_framework import serializers
from Vehicles.models import Vehicle, VehicleImage
from insurance.models import Assure
import base64
import six
import uuid
from django.core.files.base import ContentFile

class Base64ImageField(serializers.ImageField):
    """ A custom field to handle base64-encoded images """

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate a unique file name
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = f"{file_name}.{file_extension}"
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        # Return file extension depending on file type
        import imghdr
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


# class VehicleImageSerializer(serializers.ModelSerializer):
#     image = Base64ImageField()

#     class Meta:
#         model = VehicleImage
#         fields = ['id', 'image']


class VehicleSerializer(serializers.ModelSerializer):
    assure = AssureSerializer()  # Nested AssureSerializer
    image = Base64ImageField()

    class Meta:
        model = Vehicle
        fields = ['id', 'marque', 'type', 'model', 'date_fabrication', 'assure', 'user', 'image']

    def create(self, validated_data):
        assure_data = validated_data.pop('assure')
        # images_data = validated_data.pop('image', [])

        # Create or update Assure
        assure, created = Assure.objects.update_or_create(
            nom=assure_data['nom'],
            prenom=assure_data['prenom'],
            defaults=assure_data
        )

        # Create the vehicle
        vehicle = Vehicle.objects.create(assure=assure, **validated_data)

        # Save multiple images
        # for image_data in images_data:
        #     VehicleImage.objects.create(vehicle=vehicle, **image_data)

        return vehicle

    def update(self, instance, validated_data):
        assure_data = validated_data.pop('assure', None)
        images_data = validated_data.pop('images', [])

        # Update assure if provided
        if assure_data:
            assure, created = Assure.objects.update_or_create(
                nom=assure_data['nom'],
                prenom=assure_data['prenom'],
                defaults=assure_data
            )
            instance.assure = assure

        # Update vehicle fields
        instance.marque = validated_data.get('marque', instance.marque)
        instance.type = validated_data.get('type', instance.type)
        instance.model = validated_data.get('model', instance.model)
        instance.date_fabrication = validated_data.get('date_fabrication', instance.date_fabrication)
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        # Clear and update images
        instance.vehicleimage_set.all().delete()  # Clear existing images
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=instance, **image_data)

        return instance
