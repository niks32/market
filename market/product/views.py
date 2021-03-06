from django.shortcuts           import get_object_or_404, redirect
from django.template.response   import TemplateResponse
from django.http                import HttpResponsePermanentRedirect
from django.contrib             import messages   # Для эксперемента

from market.cart import Cart
from market.cart import forms

from .forms                     import get_form_class_for_product
from .models.core_models        import Category, Product
from .models.variants import StockedProduct, ProductVariant

import logging

def get_related_products(product):
    if not product.collection:
        return []
    related_products = Product.odjects.filter(collection=product.collection)
    related_products = related_products.perfetch_related('images')
    return related_products

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

    if form.is_valid():
        if form.cleaned_data['quantity']:
            msg = ('Added %(product)s to your cart.') % {
                'product': product}
            messages.success(request, msg)
        form.save()
        return redirect('product:details', slug=slug, product_id=product_id)
    template_name = 'product/details_%s.html' % (
        type(product).__name__.lower(),)
    templates = [template_name, 'product/details.html']
    #related_products = get_related_products(product)
    return TemplateResponse(
        request, templates,
        {'product': product, 'form': form})
         #'related_products': related_products})

'''
    if request.POST:
        #logging.debug('form_valid(): '+str(form.is_valid()))
        #field_errors = [ (field.label, field.errors) for field in form]
        #form.save()
        msq = ('добавлен в корзину.')
        messages.success(request, msq)
        form.save()
'''