from django.contrib import admin

from .models.core_models import Category

from mptt.admin import MPTTModelAdmin

class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category


admin.site.register(Category, MPTTModelAdmin)

