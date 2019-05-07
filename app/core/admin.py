
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
# Note _ is the convention to convert strings into readable text in py
# This would be particularly useful if we wanted to have translations
# We would save the conversion files and then it would change the
# text appropriately
from core import models

# The django admin needs to be adjusted to accommodated for our custom
# User model.


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    # Customize sections in fieldsets for our change and create page
    # to support the custom user model
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    # If we wanted to add logout date we would just add it above.


admin.site.register(models.User, UserAdmin)