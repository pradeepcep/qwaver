from django.shortcuts import render


def about(request):
    return render(request, 'queries/about.html', {'title': 'About'})