from categoria.models import Categoria
from django.shortcuts import get_object_or_404, redirect, render
import requests
from django.http import HttpResponse
from produto.models import Produto
from produto.forms import PesquisaProdutoForm, PesquisaPorCodigoForm, ProdutoForm, ProdutoCategoriaForm, QuantidadeForm
from decimal import Decimal
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required


def getFromBling(codigo):
    # busca produto no bling e retorna como json se for encontrado
    payload = {'apikey': 'e5f8af5a3039686600cd5df81b77bbf244abfacc52bb94424df874630b20384f07939108',
               'imagem': 'S'}
    produto = requests.get(
        f'https://bling.com.br/Api/v2/produto/{codigo}/json/', params=payload).json()
    print("antes do try")
    try:
        jsonProduto = produto['retorno']['produtos']
        print(jsonProduto)
        jsonProduto[0]['produto']['preco'] = '%.2f' % float(
            jsonProduto[0]['produto']['preco'])
        jsonProduto[0]['produto']['preco'] = jsonProduto[0]['produto']['preco'].replace(
            ".", ",")
        codigoErro = "Sucesso"

    except KeyError:
        print("produto não encontrado no bling")
        codigoErro = "Falha"
        return None
    try:
        jsonProduto[0]['produto']['camposCustomizados']['m2PorCaixa']
    except:
        jsonProduto[0]['produto']['camposCustomizados'] = {'m2PorCaixa': 1}
    try:
        jsonProduto[0]['produto']['imagem'][0]['link']
    except:
        jsonProduto[0]['produto']['imagem'].append({'link': ""})
    print("fim do get")
    return jsonProduto


@permission_required("administrativo")
def listaProdutoBling(request):
    # lista o codigo de todos os produtos do bling
    url = 'https://bling.com.br/Api/v2/produtos/page=1/json/'
    payload = {'apikey': 'e5f8af5a3039686600cd5df81b77bbf244abfacc52bb94424df874630b20384f07939108',
               'imagem': 'S'}
    page = 1
    produtosJson = {'produtos': []}
    c = 0
    while True:
        urlRequisitada = f'https://bling.com.br/Api/v2/produtos/page={page}/json/'
        produtos = requests.get(
            f'https://bling.com.br/Api/v2/produtos/page={page}/json/', params=payload)
        try:
            jsonAtual = produtos.json()
            for item in jsonAtual['retorno']['produtos']:
                item['numero'] = c
                produtosJson['produtos'].append(item)
                if(c == 0):
                    print(item)
                c += 1
            page += 1
        except KeyError:
            break
    print(c)
    return render(request, 'produto/index.html', {'produtos': produtosJson})


@permission_required("administrativo")
def buscaProdutoBling(request, codigo):
    # view de busca do produto por codigo para cadastro no bling
    print(codigo)
    url = f'https://bling.com.br/Api/v2/produto/{codigo}/json/'
    print(url)
    payload = {'apikey': 'e5f8af5a3039686600cd5df81b77bbf244abfacc52bb94424df874630b20384f07939108',
               'imagem': 'S'}
    produto = requests.get(url, params=payload).json()
    try:
        jsonProduto = produto['retorno']['produtos']
        codigoErro = "Sucesso"
    except:
        jsonProduto = {}
        codigoErro = "Falha"
    print(codigoErro)
    return render(request, 'produto/pagina.html', {'produto': jsonProduto, 'codigoErro': codigoErro})


@permission_required("administrativo")
def cadastraProdutoPorCodigo(request):
    # cadastra o produto já buscado no bling com os dados de lá
    print("cadastro por codigo")
    produtoDicionario = ""
    if request.GET:
        print("é get")
        try:
            del request.session['codigoSelecionado']
        except KeyError:
            pass

        formCodigo = PesquisaPorCodigoForm(request.GET)
        if formCodigo.is_valid():
            codigo = formCodigo.cleaned_data['codigo']
            print(f"{codigo} é valido no form")
            produto = getFromBling(codigo)
            if not produto:
                print("produto não encontrado no bling")
                formCodigo = PesquisaPorCodigoForm()
                messages.add_message(
                    request, messages.ERROR, 'Produto não encontrado!')
                return render(request, 'produto/cadastroPorCodigo.html', {'form': formCodigo, 'produto': ""})

            produtoDicionario = {"codigo": produto[0]['produto']['codigo'],
                                 "nome": produto[0]['produto']['descricao'],
                                 "marca": produto[0]['produto']['marca'],
                                 "imagem": produto[0]['produto']['imagem'][0]['link'],
                                 "disponivel": True,
                                 "preco": produto[0]['produto']['preco'],
                                 "altura": produto[0]['produto']['alturaProduto'],
                                 "largura": produto[0]['produto']['larguraProduto'],
                                 "profundidade": produto[0]['produto']['profundidadeProduto'],
                                 "pesoBruto": produto[0]['produto']['pesoBruto'],
                                 "unidadesPorCaixa": produto[0]['produto']['itensPorCaixa'],
                                 "multiploDeVenda": produto[0]['produto']['camposCustomizados']['m2PorCaixa'],
                                 "unidadeDeVenda": produto[0]['produto']['unidade'],
                                 "descricao": produto[0]['produto']['descricaoCurta'],
                                 }

            request.session['codigoSelecionado'] = produtoDicionario['codigo']
            print("request é:")
            print(
                f"{request.session['codigoSelecionado']} custa {produtoDicionario['preco']}")
    elif request.POST:
        print("é um post")
        formCategoria = ProdutoCategoriaForm(request.POST)
        categoria = None
        if formCategoria.is_valid():
            print(type(formCategoria.cleaned_data['categoria']))
            categoria = formCategoria.cleaned_data['categoria']
        try:
            produto = get_object_or_404(
                Produto, codigo=request.session['codigoSelecionado'])
            messages.add_message(
                request, messages.ERROR, f'O produto {produto.codigo} já está cadastrado no sistema!')
        except:
            produto = getFromBling(request.session['codigoSelecionado'])
            del request.session['codigoSelecionado']
            if not produto:
                formCodigo = PesquisaPorCodigoForm()
                return render(request, 'produto/cadastroPorCodigo.html', {'form': formCodigo, 'produto': ""})

            produtoBling = Produto(codigo=produto[0]['produto']['codigo'],
                                   nome=produto[0]['produto']['descricao'],
                                   marca=produto[0]['produto']['marca'],
                                   imagem=produto[0]['produto']['imagem'][0]['link'],
                                   disponivel=True,
                                   preco=float(
                                       produto[0]['produto']['preco'].replace(",", ".")),
                                   altura=float(
                                       produto[0]['produto']['alturaProduto']),
                                   largura=float(
                                       produto[0]['produto']['larguraProduto']),
                                   profundidade=float(
                                       produto[0]['produto']['profundidadeProduto']),
                                   pesoBruto=float(
                                       produto[0]['produto']['pesoBruto']),
                                   unidadesPorCaixa=float(
                                       produto[0]['produto']['itensPorCaixa']),
                                   unidadeDeVenda=produto[0]['produto']['unidade'],
                                   # colocar vinculado a categoria
                                   multiploDeVenda=produto[0]['produto']['camposCustomizados']['m2PorCaixa'],
                                   descricao=produto[0]['produto']['descricaoCurta'],
                                   categoria=categoria,
                                   )
            produtoBling.save()
            messages.add_message(
                request, messages.SUCCESS, f'O produto {produtoBling.codigo} foi cadastrado no com sucesso sistema!')
        formCodigo = PesquisaPorCodigoForm()
    else:
        print("request inicial")
        try:
            del request.session['codigoSelecionado']
        except KeyError:
            pass
        formCodigo = PesquisaPorCodigoForm()
    formCategoria = ProdutoCategoriaForm()
    print(produtoDicionario)
    return render(request, 'produto/cadastroPorCodigo.html', {'form': formCodigo, 'formCategoria': formCategoria,  'produto': produtoDicionario})

def paginaProduto(request, codigo, slugProduto):
    produto = get_object_or_404(Produto, codigo=codigo)
    produto.descricao = produto.descricao.splitlines()
    formQuantidade = QuantidadeForm(multiploDeVenda=produto.multiploDeVenda)
    categoriasProduto = []
    categoria = produto.categoria
    while(categoria):
        print(f"{categoria} tem id {categoria.id}")
        categoriasProduto.insert(0, categoria)
        categoria = categoria.categoriaPai
    print(categoriasProduto)
    if request.POST:
        mensagem = f"Olá, tenho interesse em: {request.POST.get('quantidade')} {produto.unidadeDeVenda} do produto: {produto.nome}"
        print(mensagem)
        return redirect(f"https://api.whatsapp.com/send?phone=5521995441122&text={mensagem}")

    return render(request, 'produto/paginaProduto.html', {'produto': produto, 'formQuantidade': formQuantidade, 'categoriasProduto': categoriasProduto})


def listaProduto(request):
    form = PesquisaProdutoForm(request.GET)
    if form.is_valid():
        nome = form.cleaned_data['nome']
        produtos = Produto.objects.filter(nome__icontains=nome)
        paginator = Paginator(produtos, 24)
        pagina = request.GET.get('pagina')
        pageObject = paginator.get_page(pagina)
        print(produtos)
        print(pageObject)
        return render(request, 'produto/listaProduto.html', {'produtos': pageObject, 'form': form, 'nomePesquisado': nome})
    else:
        raise ValueError(
            "Ocorreu um erro inesperado ao tentar recuperar um produto....")




@permission_required("administrativo")
def painelAdmin(request):
    # painel Admin de produto
    print("passou aqui pela view")
    form = PesquisaProdutoForm(request.GET)
    if form.is_valid():
        print("form é valido")
        nome = form.cleaned_data['nome']
        produtos = Produto.objects.filter(nome__icontains=nome)
        paginator = Paginator(produtos, 12)
        pagina = request.GET.get('pagina')
        pageObject = paginator.get_page(pagina)
        return render(request, 'produto/painelAdmin.html', {'produtos': pageObject, 'form': form, 'nomePesquisado': nome})
    else:
        raise ValueError(
            "Ocorreu um erro inesperado ao tentar recuperar um produto....")

@permission_required("administrativo")
def cadastraProduto(request):
    if request.POST:
        idProduto = request.session.get('produtoEditado')
        print('idProduto na sessão = ' + str(idProduto))
        if idProduto:
            produto = get_object_or_404(Produto, pk=idProduto)
            produtoForm = ProdutoForm(request.POST, instance=produto)
        else:
            produtoForm = ProdutoForm(request.POST)

        if produtoForm.is_valid():
            print("form válido")
            produto = produtoForm.save(commit=False)
            produto.save()
            if idProduto:
                messages.add_message(request, messages.SUCCESS, 'Produto alterado com sucesso!')
                del request.session['produtoEditado']
            else:
                messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso!')

            return redirect(produto.getAbsoluteUrl())
    else:
        try:
            del request.session['produtoEditado']
        except KeyError:
            pass
        produtoForm = ProdutoForm()

    return render(request, 'produto/cadastroProduto.html', {'form': produtoForm})

@permission_required("administrativo")
def editaProduto(request, codigo, slugProduto):
    produto = get_object_or_404(Produto, pk=codigo)
    produtoForm = ProdutoForm(instance=produto)
    request.session['produtoEditado'] = codigo
    return render(request, 'produto/cadastroProduto.html', {'form': produtoForm})

@permission_required("administrativo")
def removeProduto(request, codigo):
    # remove o produto com esse codigo do banco de dados
    produto = get_object_or_404(Produto, pk=codigo)
    nome = produto.nome
    produto.delete()
    messages.add_message(request, messages.SUCCESS,
                         f'O produto {nome} foi removido com sucesso.')
    return redirect('produto:painelAdminProduto')

@permission_required("administrativo")
def sincronizaPrecoProduto(request, codigo):
    # remove o produto com esse codigo do banco de dados
    produto = get_object_or_404(Produto, pk=codigo)
    nome = produto.nome
    precoAntigo = produto.preco
    produtoBling = getFromBling(codigo)
    if produtoBling:
        produto.preco = str(
            produtoBling[0]['produto']['preco']).replace(',', '.')
        produto.save()
        messages.add_message(request, messages.SUCCESS,
                             f'O preço do produto {nome} foi atualizado com sucesso de R$ {precoAntigo} para R$ {produto.preco}.')
    else:
        messages.add_message(
            request, messages.ERROR, f'O produto {nome} não foi encontrado no bling e por isso não pode ter seu preço atualizado.')
    return redirect('produto:painelAdminProduto')
