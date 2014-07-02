from django.shortcuts           import get_object_or_404
from django.template.response   import TemplateResponse
from django.http                import HttpResponsePermanentRedirect

from market.cart import Cart

from .forms                     import get_form_class_for_product
from .models.core_models        import Category, Product


import logging


def category(request):
    """
    Отображение категорий
    """
    ctx = {'category': Category.objects.filter(parent_id=None)}
    return TemplateResponse(request, "category/category.html", ctx)


def category_index(request, slug):
    '''
    Отображение подкатегорий и объектов, кот. они содержат
    '''
    cat = get_object_or_404(Category, slug=slug)
    products = cat.products.all()
    #   если у категории есть подкатегории их тоже выдираем
    subcat = []
    if cat.parent_id is not None:
        list = Category.objects.filter(id=cat.id)
        subcat.append(list[0])
        while (list[0].parent_id != None):
            list = Category.objects.filter(id=list[0].parent_id)
            subcat.append(list[0])
            subcat.reverse()
    else:
        subcat.append(cat)

    ctx = {
        'products': products, 'breed_parent': subcat, 'category': cat.children.all(),
    }
    return TemplateResponse(request, 'category/index.html',  ctx)


def product_details(request, slug, product_id):
    '''
    Отображение отдельного продукта
    '''
    product = get_object_or_404(Product.objects.select_subclasses(), id=product_id)
    if product.get_slug() != slug:
        return HttpResponsePermanentRedirect(product.get_absolute_url())

    form_class = get_form_class_for_product(product)                         #valveform
    cart = Cart.for_session_cart(request.cart)
    form = form_class(cart=cart, product=product, data=request.POST or None) #VavleForm() init

    if request.POST:
        logging.debug('form_valid(): '+str(form.is_valid()))
        #field_errors = [ (field.label, field.errors) for field in form]


    ctx = {'product': product, 'form': form}

    return TemplateResponse(request, 'product/details.html', ctx)