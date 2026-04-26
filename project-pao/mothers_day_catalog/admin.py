from django.contrib import admin

from .models import MothersDayProduct


@admin.register(MothersDayProduct)
class MothersDayProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'display_order', 'updated_at')
    list_editable = ('is_active', 'display_order')
    search_fields = ('name', 'description')
    ordering = ('display_order', '-created_at')
