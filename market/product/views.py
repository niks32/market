from django.shortcuts           import get_object_or_404
from django.template.response   import TemplateResponse


from .models.core_models        import Category, Product


def category(request, id = None ):
    ctx = { 'category' : Category.objects.filter( parent_id = id ) }
    return TemplateResponse(request, "category/category.html", ctx)


def product_details(request, slug, product_id):
    pass

def category_index(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    print("HEY HEY SLUG: "+str(cat.id))
    products = cat.products.all()
    if products.count() == 0:
        return category(request, cat.id)
    return TemplateResponse(
        request, 'category/index.html',
        {'products': products, 'category': cat})