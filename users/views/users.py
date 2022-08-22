from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import UserOrganization, Invitation


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            messages.success(request, f'Your account has been created!')
            resolve_invitations(user, request)
            login(request, user)
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('queries-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def resolve_invitations(user, request):
    invitations = Invitation.objects.filter(email__iexact=user.email)

    if len(invitations) > 0:
        # set one of these as the selected organization on the user profile
        user.profile.selected_organization = invitations.first().organization
        user.profile.save()
        # add for each invitation
        for invitation in invitations:
            user_org = UserOrganization.objects.create(user=user, organization=invitation.organization)
            user_org.save()
            # we don't need the invitation anymore
            invitation.delete()
            messages.success(request, f'You have been added to the organization {invitation.organization.name}')



@login_required
def profile(request):
    user_orgs = UserOrganization.objects.filter(user=request.user)
    # https://stackoverflow.com/questions/39702538/python-converting-a-queryset-in-a-list-of-tuples
    # converting the queryset to list of tuples
    orgs = [(q.organization.pk, q.organization.name) for q in user_orgs]
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        p_form.fields['selected_organization'].choices = orgs
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        p_form.fields['selected_organization'].choices = orgs

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
