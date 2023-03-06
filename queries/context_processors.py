from users.models import UserOrganization


def add_context(request):
    context = {}
    user = request.user
    if user is not None \
            and not request.user.is_anonymous \
            and request.user.profile is not None \
            and request.user.profile.selected_organization is not None:
        org = request.user.profile.selected_organization
        user_org = UserOrganization.objects.get(user=user, organization=org)
        context = {
            'user_level': user_org.user_level
        }
    return context
