from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect


def terms_of_service(request):
    latest_tos = settings.LATEST_TOS_VERSION if (settings.LATEST_TOS_VERSION and settings.LATEST_TOS_VERSION > 0) else 1

    if request.method == 'POST' and request.POST.get('accept') == 'yes':
        profile = request.user.profile
        profile.latest_tos_agreed_to = latest_tos
        profile.save()
        messages.success(request, 'You have agreed to the latest Terms of Service. You may now continue using Qwaver.')
        return redirect('queries-home')

    return render(request, f'queries/static/tos/{latest_tos}.html', context={
        'latest_tos': latest_tos,
        'current_tos': request.user.profile.latest_tos_agreed_to,
    })
