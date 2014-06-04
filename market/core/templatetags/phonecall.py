from django.template        import Library
from django.template.loader import render_to_string


register = Library()

from ..models import GetCallModel

@register.simple_tag(takes_context=True)
def phonecall_count(context):
    count = GetCallModel.objects.count()
    return render_to_string("phonecall/phonecall.html",{'count': count}, context_instance=context)