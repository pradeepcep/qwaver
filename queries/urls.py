from django.urls import path
from .views import (
    QueryListView,
    QueryDetailView,
    QueryCreateView,
    QueryUpdateView,
    QueryDeleteView,
    UserQueryListView
)
from . import views

urlpatterns = [
    path('', QueryListView.as_view(), name='queries-home'),
    path('user/<str:username>', UserQueryListView.as_view(), name='user-queries'),
    path('query/<int:pk>/', QueryDetailView.as_view(), name='query-detail'),
    path('query/new/', QueryCreateView.as_view(), name='query-create'),
    path('query/<int:pk>/update/', QueryUpdateView.as_view(), name='query-update'),
    path('query/<int:pk>/delete/', QueryDeleteView.as_view(), name='query-delete'),
    path('about/', views.about, name='queries-about'),
]
