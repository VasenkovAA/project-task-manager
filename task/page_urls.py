from django.urls import path

from task.views.view_pages import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
