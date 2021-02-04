from django.contrib import admin
from .models import *
import random

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'preco', 'disponivel']
    search_fields = ['nome']
    save_as = True

admin.site.register(Produto, ProdutoAdmin)
