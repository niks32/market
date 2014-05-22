from django               import    template
from ..models.core_models import    Category

register = template.Library()

@register.inclusion_tag('category/_list.html')
def categories_list():
    return {'categories': Category.objects.all()}