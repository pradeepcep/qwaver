from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DeleteView
)

from queries.common.access import user_can_access_org
from users.models import Invitation, UserOrganization


# TODO: tests
#  user creates invite, but doesn't have self.request.user.profile.selected_organization:
#    404 returned
#  User creates invite, no user with that invitation email exists yet:
#    Invitation is created
#  user creates invite, a user with that invitation email does exist:
#    UserOrganization is created for the invited user in
#      the organization self.request.user.profile.selected_organization
#    The invitation is deleted
#  users.py resolve_invitations:
#  A new user registers and their email matches multiple invitations:
#    A UserOrganization is created for each invitation
#    the profile.selected_organization for the new user is one of the new UserOrganization objects
#    each invitation for that user is deleted

class InvitationListView(LoginRequiredMixin, ListView):
    model = Invitation
    template_name = 'users/invitation_list.html'

    def get_queryset(self):
        # get or 404 if creating user has no org on profile
        selected_organization = self.request.user.profile.selected_organization
        if selected_organization is None:
            raise Http404("No Organization selected in user profile")
        invitations = Invitation.objects.filter(organization=selected_organization)
        return invitations


class InvitationCreateView(LoginRequiredMixin, CreateView):
    model = Invitation
    fields = ['email']

    def get_success_url(self):
        user = self.request.user
        org = self.request.user.profile.selected_organization

        invitation = self.object
        # first check if the user already exists.  If so, create that link and delete the invite
        # TODO add email validation and only get invited users who have validated.
        #  This keeps bad actors from guessing a user email address and getting the invite
        invited_user = User.objects.get(email=invitation.email)
        if invited_user is not None:
            invited_user_org = UserOrganization.objects.get(user=invited_user,organization=org)
            if invited_user_org is not None:
                invitation.delete()

        invitation.creator = user
        invitation.organization = org
        invitation.save()
        return reverse('invitation-list')


class InvitationEditView(LoginRequiredMixin, UpdateView):
    model = Invitation
    fields = ['email']

    def get_object(self, queryset=None):
        obj = super().get_object()
        # we do not want a user to edit an invitation for an org to which they do not belong
        user_can_access_org(self.request.user, obj.organization)
        return obj

    def get_success_url(self):
        return reverse('invitation-list')


class InvitationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invitation

    # TODO: this is a duplicate of get_object in InvitationEditView.  reuse?
    def test_func(self):
        print("here in InvitationDeleteView")
        obj = super().get_object()
        # we do not want a user to edit an invitation for an org to which they do not belong
        user_can_access_org(self.request.user, obj.organization)
        # this return won't be reached if the user cannot access the org
        return True

    def get_success_url(self):
        return reverse('invitation-list')
