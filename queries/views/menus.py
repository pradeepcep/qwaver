from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from users.models import Organization

query_ordering_most_viewed = (1, "Most viewed")
query_ordering_least_viewed = (2, "Least viewed")
query_ordering_most_run = (3, "Most run")
query_ordering_recently_run = (4, "Recently run")
query_ordering_recently_added = (5, "Recently added")
query_ordering_recently_viewed = (6, "Recently viewed")

query_orderings = [
    query_ordering_most_run,
    query_ordering_recently_run,
    query_ordering_recently_added,
    query_ordering_recently_viewed
]


@login_required
def query_ordering(request, ordering):
    request.user.profile.query_ordering = ordering
    request.user.profile.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def select_organization(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    request.user.profile.selected_organization = organization
    request.user.profile.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
