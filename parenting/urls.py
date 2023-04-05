from django.urls import path

from parenting.views import parenting_calendar

urlpatterns = [
    path('parenting/', parenting_calendar, name='parenting'),
]
