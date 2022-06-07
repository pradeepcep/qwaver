from django.urls import path
from .views import *

urlpatterns = [
    path('', QueryListView.as_view(), name='queries-home'),
    path('user/<str:username>', UserQueryListView.as_view(), name='user-queries'),
    path('result/<int:id>/', result.execute, name='result-detail'),
    path('about/', about, name='queries-about'),

    path('query/new/', QueryCreateView.as_view(), name='query-create'),
    path('query/<int:pk>/edit/', QueryEditView.as_view(), name='query-update'),
    path('query/<int:pk>/', QueryDetailView.as_view(), name='query-detail'),
    # path('query/<int:query_id>/', instance.as_view, name='query-detail'),
    path('query/<int:id>/run', result.execute, name='query-run'),
    path('query/<int:pk>/delete/', QueryDeleteView.as_view(), name='query-delete'),
    path('query/<int:pk>/clone/', QueryCloneView.as_view(), name='query-clone'),
    path('query/search/', QuerySearchView.as_view(), name='query-search'),

    path('param/new/<int:query_id>/', ParameterCreateView.as_view(), name='param-create'),
    path('param/<int:pk>/', ParameterDetailView.as_view(), name='param-detail'),
    path('param/<int:pk>/edit/', ParameterEditView.as_view(), name='param-update'),
    path('param/<int:pk>/delete/', ParameterDeleteView.as_view(), name='param-delete'),

    path('instance/new/<int:query_id>/', instance.as_view, name='instance-create'),
    path('instance/<int:pk>/', QueryCreateView.as_view(), name='instance-detail'),

    path('database/new/', DatabaseCreateView.as_view(), name='database-create'),
    path('database/<int:pk>/', DatabaseEditView.as_view(), name='database-detail'),
    path('database/<int:pk>/edit/', DatabaseEditView.as_view(), name='database-update'),
    path('databases/', DatabaseListView.as_view(), name='database-list'),
    path('database/<int:pk>/delete/', DatabaseDeleteView.as_view(), name='database-delete'),
]
