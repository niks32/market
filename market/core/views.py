from django.contrib           import messages
from django.shortcuts         import render, redirect, HttpResponse

from .forms import GetPhoneForm

def home(request):
    return render(request, 'base.html')

def work(request):
    return render(request, 'working.html')

def getphonecall(request):
    form = GetPhoneForm(data=request.POST, user=request.user)
    if request.POST:
        if form.is_valid():
            form.clean()
            messages.info(request, "Спасибо, <b>"+request.POST.get("name", "")+'</b>! Мы вам обязательно позвоним по номеру <b>'+
            request.POST.get('phone','')+'</b>')
            form.save()
        else:
            messages.warning(request, "Мы не сможем вам перезвонить, так как форма была заполнена неккоректно")
    return redirect("home:homepage")