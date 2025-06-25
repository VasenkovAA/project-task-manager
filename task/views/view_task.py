from django_filters import rest_framework as df_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from task.serializers import TaskSerializer


class TaskFilter(FilterSet):
    min_priority = df_filters.NumberFilter(field_name='priority', lookup_expr='gte')
    max_priority = df_filters.NumberFilter(field_name='priority', lookup_expr='lte')
    min_progress = df_filters.NumberFilter(field_name='progress', lookup_expr='gte')
    max_progress = df_filters.NumberFilter(field_name='progress', lookup_expr='lte')
    start_date_after = df_filters.DateTimeFilter(field_name='start_date', lookup_expr='gte')
    start_date_before = df_filters.DateTimeFilter(field_name='start_date', lookup_expr='lte')
    end_date_after = df_filters.DateTimeFilter(field_name='end_date', lookup_expr='gte')
    end_date_before = df_filters.DateTimeFilter(field_name='end_date', lookup_expr='lte')
    deadline_after = df_filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')
    deadline_before = df_filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')
    complexity_min = df_filters.NumberFilter(field_name='complexity', lookup_expr='gte')
    complexity_max = df_filters.NumberFilter(field_name='complexity', lookup_expr='lte')

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'author': ['exact'],
            'assignee': ['exact'],
            'location': ['exact'],
            'is_ready': ['exact'],
            'is_recurring': ['exact'],
            'needs_approval': ['exact'],
            'is_template': ['exact'],
            'risk_level': ['exact'],
        }

@extend_schema(tags=['Tasks'])
class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['task_name', 'description', 'cancel_reason', 'tags__name']
    ordering_fields = [
        'created_at', 'updated_at', 'start_date', 'end_date', 'deadline',
        'priority', 'progress', 'complexity'
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            user_spaces = user.spaces.all()
            queryset = queryset.filter(task_space__in=user_spaces)
        return queryset

@extend_schema(tags=['Tasks'])
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            user_spaces = user.spaces.all()
            queryset = queryset.filter(task_space__in=user_spaces)
        return queryset