# Components: data objects commonly used in templates
from queries.models import Result, Value


def users_recent_results(query, user):
    recent_results = Result.objects.filter(query=query, user=user) \
                         .order_by('-timestamp')[:15]
    results = []
    for result in recent_results:
        line = {'result': result}
        line['is_current'] = result.version_number == query.version_number
        values = list(Value.objects.filter(result=result).order_by('parameter_name'))
        line['values'] = values
        results.append(line)
    return results
