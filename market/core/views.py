from django.contrib             import messages
from django.shortcuts           import render, redirect
from django.template.response   import TemplateResponse

from .forms  import GetPhoneForm
from .models import GetCallModel

def home(request):
    return render(request, 'base.html')

def work(request):
    '''
    if request.user.is_authenticated():
        print(request.user.first_name)
    else:
        print("anon")
    user_permissions = request.user.groups.all()
    print(len(user_permissions))
    for p in user_permissions:
        print(p)
    '''
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

def phonecalls(request):
    ctx = {'calls': GetCallModel.objects.all() }
    return TemplateResponse(request, "phonecalls.html", ctx)