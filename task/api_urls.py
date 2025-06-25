from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from task.views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    FileListCreateView,
    FileRetrieveUpdateDestroyView,
    LinkListCreateView,
    LinkRetrieveUpdateDestroyView,
    LocationListCreateView,
    LocationRetrieveUpdateDestroyView,
    SpaceListCreateView,
    SpaceRetrieveUpdateDestroyView,
    StatusListCreateView,
    StatusRetrieveUpdateDestroyView,
    TaskLinkListCreateView,
    TaskLinkRetrieveUpdateDestroyView,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
)

urlpatterns = [
    # ====================== API Documentation ======================
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    # ====================== Categories ======================
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    # ====================== Files ======================
    path('files/', FileListCreateView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileRetrieveUpdateDestroyView.as_view(), name='file-detail'),
    # ====================== Links ======================
    path('links/', LinkListCreateView.as_view(), name='link-list'),
    path('links/<int:pk>/', LinkRetrieveUpdateDestroyView.as_view(), name='link-detail'),
    # ====================== Locations ======================
    path('locations/', LocationListCreateView.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationRetrieveUpdateDestroyView.as_view(), name='location-detail'),
    # ====================== Spaces ======================
    path('spaces/', SpaceListCreateView.as_view(), name='space-list'),
    path('spaces/<int:pk>/', SpaceRetrieveUpdateDestroyView.as_view(), name='space-detail'),
    # ====================== Statuses ======================
    path('statuses/', StatusListCreateView.as_view(), name='status-list'),
    path('statuses/<int:pk>/', StatusRetrieveUpdateDestroyView.as_view(), name='status-detail'),
    # ====================== Tasks ======================
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    # ====================== Task Links ======================
    path('task-links/', TaskLinkListCreateView.as_view(), name='tasklink-list'),
    path('task-links/<int:pk>/', TaskLinkRetrieveUpdateDestroyView.as_view(), name='tasklink-detail'),
    # ====================== Token ======================
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
