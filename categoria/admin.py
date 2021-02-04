from django.contrib import admin
from .models import *
# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoriaPai']
    search_fields = ['nome']
    save_as = True

admin.site.register(Categoria, CategoriaAdmin)

