from django.shortcuts import render

def home(request):
    return render(request, 'base.html')

def work(request):
    return render(request, 'working.html')