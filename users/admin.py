from django.contrib import admin
from .models import Profile, UserOrganization, Invitation

admin.site.register(Profile)
admin.site.register(UserOrganization)
admin.site.register(Invitation)

