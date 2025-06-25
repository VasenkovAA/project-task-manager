from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from task.models import Location
from task.serializers import LocationSerializer


@extend_schema(tags=['Locations'])
class LocationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

@extend_schema(tags=['Locations'])
class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer