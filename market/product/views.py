from django.shortcuts           import get_object_or_404
from django.template.response   import TemplateResponse



from .models.core_models        import Category, Product


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

    print("LEN: "+str(len(subcat)))
    ctx = {
        'products': products, 'breed_parent': subcat, 'category': cat.children.all(),
    }
    return TemplateResponse(request, 'category/index.html',  ctx)

def product_details(request, slug, product_id):
    pass