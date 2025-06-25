from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from task.models import Category
from task.serializers import CategorySerializer


@extend_schema(tags=['Categories'])
class CategoryListCreateView(generics.ListCreateAPIView):
    """get: Список всех категорий | post: Создать новую категорию"""
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema(tags=['Categories'])
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """get: Детали | put: Обновить | patch: Частично обновить | delete: Удалить"""
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer