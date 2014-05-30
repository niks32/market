from django.contrib           import messages
from django.shortcuts         import render, redirect

def home(request):
    return render(request, 'base.html')

def work(request):
    return render(request, 'working.html')

def getphonecall(request):
    messages.info(request, "FUCK YEAH")
    return redirect("home:homepage")