from django.shortcuts           import get_object_or_404
from django.template.response   import TemplateResponse
from django.http                import HttpResponsePermanentRedirect


from .forms                     import get_form_class_for_product
from .models.core_models        import Category, Product, ProductImage


def category(request):
    ctx = { 'category' : Category.objects.filter( parent_id = None ) }
    return TemplateResponse(request, "category/category.html", ctx)


def category_index(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    products = cat.products.all()
    #   если у категории есть подкатегории их тоже выдираем
    subcat = []
    if cat.parent_id != None:
        list = Category.objects.filter( id = cat.id )
        subcat.append(list[0])
        while (list[0].parent_id != None):
            list = Category.objects.filter( id = list[0].parent_id )
            subcat.append(list[0])
            subcat.reverse()
    else:
        subcat.append(cat)

    ctx = {
        'products': products, 'breed_parent': subcat, 'category': cat.children.all(),
    }
    return TemplateResponse(request, 'category/index.html',  ctx)

def product_details(request, slug, product_id):
    product = get_object_or_404(Product.objects.select_subclasses(), id=product_id)
    if product.get_slug() != slug:
        return HttpResponsePermanentRedirect(product.get_absolute_url())

    #for item in product.variants.all():
    #    print(item.dn)

    form = get_form_class_for_product(product)

    ctx = { 'product': product, 'form': form }

    return TemplateResponse(request, 'product/details.html', ctx)