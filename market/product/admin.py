from django.contrib import admin

from .models.core_models import Category, ProductImage, Product_Product
from .models.products    import Valve, ValveVariant
#from .models.images      import ProductImage

from .forms import ProductVariantInline, ValveAdminForm

from mptt.admin import MPTTModelAdmin

class ImageAdminInline(admin.StackedInline):
    model = ProductImage

class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
    list_editable = False

    list_display = ['name', 'description']

class ValveVariant(admin.StackedInline):
    model   = ValveVariant
    formset = ProductVariantInline
    price = Price

class ValveAdmin(admin.ModelAdmin):
    form = ValveAdminForm
    inlines = [ValveVariant, ImageAdminInline]
    list_display = ['name', 'category']
    search_fields = ['name']

<<<<<<< Updated upstream
=======
class Price(admin.StackedInline): #сюда прайс
    model = Product_Product
    inlines = ValveVariant
    list_editable = True

>>>>>>> Stashed changes
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Valve, ValveAdmin)