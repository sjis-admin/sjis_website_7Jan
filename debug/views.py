from django.shortcuts import render

def debug_view(request):
    return render(request, 'debug/debug.html', {'my_string': 'Hello, world!'})