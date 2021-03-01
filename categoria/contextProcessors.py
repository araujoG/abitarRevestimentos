from categoria.models import Categoria

def categorias(request):
    categorias = Categoria.objects.all()
    listaDict = []
    for cat in categorias:
        if(not cat.categoriaPai):
            listaDict.append({'categoria':cat, 'listaFilhos': cat.categoriasFilhas()})
    return {
        'categoriasDoSite': listaDict ,
    }