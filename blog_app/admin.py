from django.contrib import admin
from .models import Filter

# Register your models here.


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'text_request',)}
    fields = ('name', 'slug', 'author', 'text_request')
