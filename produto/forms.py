from django import forms
from produto.models import Produto
from django.core.validators import MaxValueValidator, RegexValidator

class PesquisaProdutoForm(forms.Form):
    
    nome = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control mr-0', 'placeholder':'Pesquisar', 'aria-label':'Pesquisar'}),
        required = False,
    )

class PesquisaPorCodigoForm(forms.Form):
    
    codigo = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control mr-0', 'placeholder':'Digite o Código do Produto', 'aria-label':'Digite o Código do Produto'}),
        required = True,
        max_length = 20,
    )

class ProdutoForm(forms.ModelForm):
    
    class Meta:
        model = Produto
        fields = ("codigo","nome","marca","imagem","disponivel","preco","altura", "largura", "profundidade", "unidadesPorCaixa", "unidadeDeVenda", "multiploDeVenda", "descricao", "slug")
        localized_fields = ("preco", "mutiploDeVenda")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProdutoCategoriaForm(forms.ModelForm):
    
    class Meta:
        model = Produto
        fields = ("categoria",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['categoria'].empty_label='--- Selecione uma categoria ---'
        self.fields['categoria'].widget.attrs.update({'class': 'form-control custom-select','id':'inputCategoria'})

class QuantidadeForm(forms.Form):
    def __init__(self, *args, **kwargs):

        step = kwargs.pop('multiploDeVenda')
        super(QuantidadeForm, self).__init__(*args, **kwargs)
        self.fields['quantidade'].widget.attrs.update({'data-step': step, 'value' : step, 'min' : step})

    quantidade = forms.CharField(
        widget = forms.TextInput(attrs={'id': 'qauntidade1', 'type': "text", 'max' : "9999" , 'class': 'form-control', 'placeholder':'Digite o Código do Produto', 'aria-label':'Digite o Código do Produto'}),
        required = True,
        max_length = 20,
    )