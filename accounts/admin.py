from django.contrib import admin
from . models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_filter = ('is_active', 'is_staff',)

admin.site.register(CustomUser, CustomUserAdmin)


