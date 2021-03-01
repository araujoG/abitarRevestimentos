from categoria.models import Categoria
from django.shortcuts import render
from django.core.paginator import Paginator


# Create your views here.
def paginaCategoria(request, slug):
    categoria = Categoria.objects.get(slug=slug)
    produtos = Categoria.objects.get(slug=slug).produto_set.all()
    for categoriaFilha in categoria.categoria_set.all():
        produtos = produtos | (Categoria.objects.get(slug=categoriaFilha.slug).produto_set.all())
        print(f"a categoria {categoriaFilha} tem {produtos}")
    paginator = Paginator(produtos, 24)
    pagina = request.GET.get('pagina')
    pageObject = paginator.get_page(pagina)
    print(produtos)
    print(pageObject)
    return render(request, 'produto/listaProduto.html', {'produtos': pageObject, 'categoriaAtual': categoria})

