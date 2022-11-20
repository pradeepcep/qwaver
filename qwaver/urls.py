"""qwaver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('queries/', include('queries.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500

# handler400 = 'qwaver.views.bad_request'
# handler403 = 'qwaver.views.permission_denied'
# handler404 = 'qwaver.views.page_not_found'
handler500 = 'queries.views.handler500'

urlpatterns = [
    path('', include('queries.urls')),
    path('', include('users.urls')),
]
# appears to be required on production as well as local
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
