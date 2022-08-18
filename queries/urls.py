from django.urls import path
from .views import *
from .views.result import ResultDetailView

urlpatterns = [
    path('', QueryListView.as_view(), name='queries-home'),
    path('user/<str:username>', UserQueryListView.as_view(), name='user-queries'),

    path('query/new/', QueryCreateView.as_view(), name='query-create'),
    path('query/<int:pk>/', QueryDetailView.as_view(), name='query-detail'),
    path('query/<int:pk>/edit/', QueryEditView.as_view(), name='query-update'),
    path('query/<int:id>/run/', result.execute, name='query-run'),
    path('query/<int:pk>/delete/', QueryDeleteView.as_view(), name='query-delete'),
    path('query/<int:pk>/clone/', QueryCloneView.as_view(), name='query-clone'),

    path('result/<int:pk>/', ResultDetailView.as_view(), name='result-detail'),

    path('param/<int:pk>/edit/', ParameterEditView.as_view(), name='param-update'),

    path('database/new/', DatabaseCreateView.as_view(), name='database-create'),
    path('database/<int:pk>/', DatabaseEditView.as_view(), name='database-detail'),
    path('database/<int:pk>/edit/', DatabaseEditView.as_view(), name='database-update'),
    path('databases/', DatabaseListView.as_view(), name='database-list'),
    path('database/<int:pk>/delete/', DatabaseDeleteView.as_view(), name='database-delete'),

    path('search/', QuerySearchView.as_view(), name='query-search'),
    path('searches/', UserSearchListView.as_view(), name='query-searches'),

]
