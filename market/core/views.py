from django.shortcuts         import render
from django.template.response import TemplateResponse

from .forms                   import GetPhoneForm

def home(request):
    form = GetPhoneForm()
    return TemplateResponse(request, 'base.html', {'form':form })

def work(request):
    return render(request, 'working.html')