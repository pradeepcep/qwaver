from django.contrib import admin
from .models import Query, Database, Parameter, Organization

admin.site.register(Query)
admin.site.register(Database)
admin.site.register(Parameter)
admin.site.register(Organization)
