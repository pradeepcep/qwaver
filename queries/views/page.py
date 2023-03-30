from django.shortcuts import render


def about(request):
    return render(request, 'queries/static/about.html', {'title': 'About'})