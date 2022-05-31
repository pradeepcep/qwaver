from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from queries.models import Instance, Query, Parameter
from queries.views import result


@login_required
def as_view(request, query_id):
    user = request.user
    query = Query.objects.get(pk=query_id)
    instance = Instance.objects.create(query=query, user=user)
    params = Parameter.objects.filter(query=query)
    if params.exists():
        context = {
            'instance': instance,
            'params': params
        }
        return render(request, 'queries/instance.html', context)
    else:
        return result.execute(request, query_id)
