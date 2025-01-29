import json
from Vehicles.models import Vehicle  # Import your Vehicle model
from Vehicles.serializers import VehicleSerializer  # Import your serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class VehicleListView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = VehicleSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        serializer = VehicleSerializer(vehicle, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleDeleteView(APIView):
    def delete(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class VehicleEditView(APIView):
    def put(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        serializer = VehicleSerializer(vehicle, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)