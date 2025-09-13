from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def about_view(request):
    #print(request)
    # return HttpResponse("<html><body>Hello World</body></html>")
    # return HttpResponse("Hello World!")
    return render(request, 'about.html')

def welcome_view(request):
    return render(request, 'core/pages/welcome.html')