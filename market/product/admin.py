from django.contrib import admin

from .models.core_models import Category
from .models.images      import ProductImage
from .models.products    import Valve, ValveVariant

from mptt.admin import MPTTModelAdmin

class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category

class ImageAdminInline(admin.StackedInline):
    model = ProductImage

class ValveVariantInline(admin.StackedInline):
    model   = ValveVariant

class ValveAdmin(admin.ModelAdmin):
    inline = [ValveVariantInline, ImageAdminInline]



admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Valve, ValveAdmin)
