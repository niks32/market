from django.shortcuts           import get_object_or_404
from django.template.response   import TemplateResponse


from .models.core_models        import Category, Product


def category(request):
    ctx = { 'category' : Category.objects.all() }
    return TemplateResponse(request, "category/category.html", ctx)


def product_details(request, slug, product_id):
    pass

def category_index(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    #products = products.prefetch_related('images')
    return TemplateResponse(
        request, 'category/index.html',
        {'products': products, 'category': category})