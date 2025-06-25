from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from task.models import Space
from task.serializers import SpaceSerializer


@extend_schema(tags=['Spaces'])
class SpaceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

@extend_schema(tags=['Spaces'])
class SpaceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer