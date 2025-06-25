from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from task.models import Status
from task.serializers import StatusSerializer


@extend_schema(tags=['Statuses'])
class StatusListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

@extend_schema(tags=['Statuses'])
class StatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer