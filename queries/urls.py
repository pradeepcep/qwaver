from django.urls import path
from .views import (
    QueryListView,
    QueryDetailView,
    QueryCreateView,
    QueryUpdateView,
    QueryDeleteView,
    UserQueryListView, DatabaseCreateView, DatabaseUpdateView, DatabaseListView
)
from . import views

urlpatterns = [
    path('', QueryListView.as_view(), name='queries-home'),
    path('user/<str:username>', UserQueryListView.as_view(), name='user-queries'),
    path('query/<int:pk>/', QueryDetailView.as_view(), name='query-detail'),
    path('query/new/', QueryCreateView.as_view(), name='query-create'),
    path('query/<int:pk>/update/', QueryUpdateView.as_view(), name='query-update'),
    path('query/<int:pk>/delete/', QueryDeleteView.as_view(), name='query-delete'),
    path('database/<int:pk>/', DatabaseUpdateView.as_view(), name='database-detail'),
    path('database/new/', DatabaseCreateView.as_view(), name='database-create'),
    path('database/<int:pk>/update/', DatabaseUpdateView.as_view(), name='database-update'),
    path('databases/', DatabaseListView.as_view(), name='database-list'),
    path('about/', views.about, name='queries-about'),
]
