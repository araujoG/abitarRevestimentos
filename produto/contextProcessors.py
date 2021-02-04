from produto.forms import PesquisaProdutoForm

def pesquisaProduto(request):
    form = PesquisaProdutoForm(request.GET)

    return {
        'pesquisa': form ,
    }