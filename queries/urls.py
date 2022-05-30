from django.urls import path
from .views import *

urlpatterns = [
    path('', QueryListView.as_view(), name='queries-home'),
    path('user/<str:username>', UserQueryListView.as_view(), name='user-queries'),
    path('result/<int:id>/', result.execute, name='result-detail'),
    path('about/', about, name='queries-about'),

    path('query/new/', QueryCreateView.as_view(), name='query-create'),
    path('query/<int:pk>/', QueryDetailView.as_view(), name='query-detail'),
    path('query/<int:pk>/update/', QueryUpdateView.as_view(), name='query-update'),
    path('query/<int:pk>/delete/', QueryDeleteView.as_view(), name='query-delete'),

    path('param/new/<int:query_id>/', ParameterCreateView.as_view(), name='param-create'),
    path('param/<int:pk>/', ParameterDetailView.as_view(), name='param-detail'),
    path('param/<int:pk>/update/', ParameterUpdateView.as_view(), name='param-update'),
    path('param/<int:pk>/delete/', ParameterDeleteView.as_view(), name='param-delete'),

    path('database/new/', DatabaseCreateView.as_view(), name='database-create'),
    path('database/<int:pk>/', DatabaseUpdateView.as_view(), name='database-detail'),
    path('database/<int:pk>/update/', DatabaseUpdateView.as_view(), name='database-update'),
    #TODO DELETE VIEW
    path('databases/', DatabaseListView.as_view(), name='database-list'),
]
