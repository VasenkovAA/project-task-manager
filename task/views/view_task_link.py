from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from task.models import TaskLink
from task.serializers import TaskLinkSerializer


@extend_schema(tags=['Task Links'])
class TaskLinkListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TaskLink.objects.all()
    serializer_class = TaskLinkSerializer

@extend_schema(tags=['Task Links'])
class TaskLinkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TaskLink.objects.all()
    serializer_class = TaskLinkSerializer