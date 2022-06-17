from django.contrib import admin

from users.models import Organization
from .models import Query, Database, Parameter


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    readonly_fields = ('id',)


admin.site.register(Query)
admin.site.register(Database)
admin.site.register(Parameter)
admin.site.register(Organization, OrganizationAdmin)
