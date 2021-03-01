from django.core.paginator import Paginator
from produto.models import Produto
from django.shortcuts import render
from produto.models import Produto
import random

def index(request):
    frase = "esta é a frase da index Abitar"
    produtos = Produto.objects.all()
    paginator = Paginator(produtos, 12)
    pagina = request.GET.get('pagina')
    pageObject = paginator.get_page(pagina)
    return render(request, 'index.html', {'produtos':pageObject})