from django.contrib import admin
from .models import Query, Database, Parameter

admin.site.register(Query)
admin.site.register(Database)
admin.site.register(Parameter)
