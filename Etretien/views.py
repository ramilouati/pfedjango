from django.shortcuts import get_object_or_404
from Etretien.models import Entretien
from Etretien.serializers import EntretiensSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class EntretienViewSet(APIView):
    def get(self, request):
        vehicle_id = request.query_params.get('vehicule')  # Get vehicle_id from query params

        if not vehicle_id:
            return Response({'error': 'Vehicle ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Query the entretiens by vehicle ID
            entretiens = Entretien.objects.filter(vehicle=vehicle_id)

            # Serialize the entretiens data
            serializer = EntretiensSerializer(entretiens, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # Handle POST request to create a new entretien
        serializer = EntretiensSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        # Handle PUT request to update an existing entretien
        entretien_id = request.data.get('id')  # Fetch the entretien ID

        if not entretien_id:
            return Response({'error': 'Entretien ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the specific Entretien object or return 404
        entretien_instance = get_object_or_404(Entretien, id=entretien_id)

        # Update the existing Entretien with new data
        serializer = EntretiensSerializer(entretien_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        # Handle DELETE request to delete an existing entretien
        entretien_id = request.data.get('id')  # Fetch the entretien ID

        if not entretien_id:
            return Response({'error': 'Entretien ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the specific Entretien object or return 404
        entretien_instance = get_object_or_404(Entretien, id=entretien_id)

        # Delete the existing Entretien
        entretien_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
