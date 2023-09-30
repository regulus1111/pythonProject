from django.shortcuts import render


def runoob(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'search_form.html', context)