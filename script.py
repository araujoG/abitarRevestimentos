from categoria.models import Categoria
from produto.models import Produto
import requests
import csv


def salvaProduto(listaCodigo):
    categoria = Categoria.objects.get(id=2)
    for codigo in listaCodigo:
        payload = {'apikey': 'e5f8af5a3039686600cd5df81b77bbf244abfacc52bb94424df874630b20384f07939108',
                   'imagem': 'S'}
        produto = requests.get(
            f'https://bling.com.br/Api/v2/produto/{codigo}/json/', params=payload).json()
        print("antes do try")
        try:
            jsonProduto = produto['retorno']['produtos']
            jsonProduto[0]['produto']['preco'] = '%.2f' % float(
                jsonProduto[0]['produto']['preco'])
            jsonProduto[0]['produto']['preco'] = jsonProduto[0]['produto']['preco'].replace(
                ".", ",")
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
        print("sucesso2")
        produto = jsonProduto
        produtoBling = Produto(codigo=produto[0]['produto']['codigo'], nome=produto[0]['produto']['descricao'], marca=produto[0]['produto']['marca'], imagem=produto[0]['produto']['imagem'][0]['link'], disponivel=True, preco=float(produto[0]['produto']['preco'].replace(",", ".")), altura=float(produto[0]['produto']['alturaProduto']), largura=float(produto[0]['produto']['larguraProduto']), profundidade=float(produto[0]['produto']['profundidadeProduto']), pesoBruto=float(produto[0]['produto']['pesoBruto']), unidadesPorCaixa=float(produto[0]['produto']['itensPorCaixa']), unidadeDeVenda=produto[0]['produto']['unidade'], multiploDeVenda=produto[0]['produto']['camposCustomizados']['m2PorCaixa'], descricao=produto[0]['produto']['descricaoCurta'], categoria=categoria,)
        print("sucesso3")
        produtoBling.save()
        print(f"{produtoBling.codigo} foi salvo")
salvaProduto(["R36022","R33023","R33026","R33021","R33027","R36024","R36020","R36023","R36021","R32031","R32024","R32028","R32027","R32029","R32012","R32021","R32025","R32023","R32030","R32020","R32026","R39010","R39011"])


with open('produtos.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    lista = []
    for row in reader:
        lista.append(row['Código'].replace("\t", ""))
