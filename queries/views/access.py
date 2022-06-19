from django.core.exceptions import PermissionDenied

from queries.domain.ActionEnum import ActionEnum
from queries.domain.TableEnum import TableEnum
from queries.models import Database, UserAction
from users.models import UserOrganization


def get_org_databases(self):
    user = self.request.user
    org = user.profile.selected_organization
    if org is None:
        raise PermissionDenied("Need a defined organization for profile of user " + user.username)
    databases = Database.objects.filter(organization=org)
    return databases


def user_can_access_query(user, query):
    user_can_access_database(user, query.database)


def user_can_access_database(user, database):
    user_orgs = UserOrganization.objects.filter(user=user)
    if any(database.organization.id == user_org.organization.id for user_org in user_orgs):
        # if a user is accessing a new org, they are now navigating within that org
        user.profile.selected_organization = database.organization
        user.profile.save()
    else:
        user_action = UserAction(
            user=user,
            organiztion=database.organization,
            row_id=database.id,
            action=ActionEnum.PERMISSION_DENIED,
            table=TableEnum.DATABASE
        )
        user_action.save()
        raise PermissionDenied(
            "user not part of the organization to which the database belongs")