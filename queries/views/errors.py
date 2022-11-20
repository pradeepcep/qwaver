from django.shortcuts import render


def handler500(request):
    context = {
        'user': request.user
    }
    return render(request, 'queries/error.html', context)
