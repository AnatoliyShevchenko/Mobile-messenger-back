# Django
from django.contrib import admin
from django.contrib.auth.hashers import make_password

# Local
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    """Admin panel for Client."""

    model = Client
    list_display = (
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'phone_number',
        'is_active', 
        'is_staff',
        'is_superuser', 
    )
    search_fields = (
        'username',
        'email',
        'phone_number'
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(
                form.cleaned_data['password']
            )
        super().save_model(request, obj, form, change)


admin.site.register(Client, ClientAdmin)

