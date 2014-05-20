from .forms                    import AdminUserAddForm, AdminUserChangeForm
from .models                   import User
from django.contrib            import admin
from django.contrib.auth.admin import (UserAdmin as BaseUserAdmin)


class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'email',
            'avatar',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'avatar')}
        ),
    )

admin.site.register(User, UserAdmin)