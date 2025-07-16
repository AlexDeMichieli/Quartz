from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'navigation/index.html')

def hello_world(request):
    return HttpResponse("Hello, World!")