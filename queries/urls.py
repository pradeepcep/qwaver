from django.urls import path
from django.views.generic import TemplateView
from .views import *
from .views.ai import query_ai_create
from .views.menus import query_ordering, select_organization
from .views.query_version import QueryVersionListView, QueryVersionRevertView
from .views.result import ResultDetailView

urlpatterns = [

    # query lists
    path('', QueryListView.as_view(), name='queries-home'),
    path('ref/<str:ref_code>', QueryListView.as_view(), name='queries-home'),
    path('user/<str:username>', UserQueryListView.as_view(), name='user-queries'),
    path('export/', query.query_export, name='query-export'),

    # static pages:
    path('privacy/', TemplateView.as_view(template_name='queries/static/privacy.html'), name='privacy'),
    path('tos/', TemplateView.as_view(template_name='queries/static/tos.html'), name='tos'),

    # queries
    path('query/new/', QueryCreateView.as_view(), name='query-create'),
    path('query/ai-create/', query_ai_create, name='query-ai-create'),
    path('query/<int:pk>/', QueryDetailView.as_view(), name='query-detail'),
    path('query/<int:pk>/edit/', QueryEditView.as_view(), name='query-update'),
    path('query/<int:query_id>/run/', result.execute, name='query-run'),
    path('query/<int:pk>/delete/', QueryDeleteView.as_view(), name='query-delete'),
    path('query/<int:pk>/clone/', QueryCloneView.as_view(), name='query-clone'),
    path('api/<int:query_id>/', result.execute_api, name='query-api'),

    # results
    path('result/<int:pk>/', ResultDetailView.as_view(), name='result-detail'),

    # parameters
    path('param/<int:pk>/edit/', ParameterEditView.as_view(), name='param-update'),

    # databases
    path('database/new/', DatabaseCreateView.as_view(), name='database-create'),
    path('database/<int:pk>/', DatabaseEditView.as_view(), name='database-detail'),
    path('database/<int:pk>/edit/', DatabaseEditView.as_view(), name='database-update'),
    path('databases/', DatabaseListView.as_view(), name='database-list'),
    path('database/<int:pk>/delete/', DatabaseDeleteView.as_view(), name='database-delete'),

    # searches
    path('search/', QuerySearchView.as_view(), name='query-search'),
    path('searches/', UserSearchListView.as_view(), name='query-searches'),

    # versions
    path('versions/<int:query_id>/', QueryVersionListView.as_view(), name='query-versions'),
    path('versions/<int:query_id>/revert/<int:v>', QueryVersionRevertView.as_view(), name='query-version-revert'),

    # loading data
    path('load/', LoadFileCreateView.as_view(), name='load'),

    # testing the front end
    path('test/', TemplateView.as_view(template_name='queries/static/index.html'), name='test-home'),
    path('test/ref/<str:ref_code>', TemplateView.as_view(template_name='queries/static/index.html'), name='test-home'),

    # menus
    path('order-by/<int:ordering>/', query_ordering, name='query-ordering'),
    path('select-org/<int:pk>/', select_organization, name='select-organization'),

]
