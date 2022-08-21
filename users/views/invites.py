from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DeleteView
)

from queries.common.access import user_can_access_org
from users.models import Invitation


class InvitationListView(LoginRequiredMixin, ListView):
    model = Invitation
    template_name = 'users/invitation_list.html'

    def get_queryset(self):
        # get or 404 if creating user has no org on profile
        selected_organization = self.request.user.profile.selected_organization
        if selected_organization is None:
            raise Http404("Selected Organization not found in user profile")
        orgs = Invitation.objects.filter(organization=selected_organization)
        return orgs


class InvitationCreateView(LoginRequiredMixin, CreateView):
    model = Invitation
    fields = ['email']

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.creator = self.request.user
        return obj

    def get_success_url(self):
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
    def get_object(self, queryset=None):
        obj = super().get_object()
        # we do not want a user to edit an invitation for an org to which they do not belong
        user_can_access_org(self.request.user, obj.organization)
        return obj

    def test_func(self):
        return True

    def get_success_url(self):
        return reverse('invitation-list')
