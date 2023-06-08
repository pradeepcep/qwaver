from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, reverse


class EmailVerificationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO: configure email server, re-enable code
        # should_verify_email = (
        #     request.user.is_authenticated and
        #     not request.user.profile.email_verified
        # )
        # is_regular_user = not (
        #     request.user.is_staff or
        #     request.user.is_superuser
        # )
        # exempted_views = [
        #     reverse('verify-email'),
        #     reverse('logout'),
        # ]
        #
        # if is_regular_user and should_verify_email:
        #     if request.path not in exempted_views:
        #         return redirect('verify-email')

        return self.get_response(request)


class TermsOfServiceCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_views = [
            reverse('tos'),
            reverse('logout'),
        ]
        should_skip_check = (
            (settings.LATEST_TOS_VERSION in (None, 0, '0')) or
            (request.path in excluded_views) or
            (request.path.startswith('/admin/')) or
            (getattr(request, 'user', None) is None) or
            (request.user.is_authenticated is False)
        )

        if should_skip_check:
            return self.get_response(request)

        if not request.user.profile.latest_tos_agreed_to:
            messages.info(request, (
                'Please review and accept our Terms of Service to continue using Qwaver.'
            ))
            return redirect('tos')

        if settings.LATEST_TOS_VERSION and request.user.profile.latest_tos_agreed_to < settings.LATEST_TOS_VERSION:
            messages.info(request, (
                'We have updated our Terms of Service. '
                'Please review and accept this latest version to continue using Qwaver.'
            ))
            return redirect('tos')

        return self.get_response(request)
