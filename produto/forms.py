from categoria.models import Categoria
from django import forms
from produto.models import Produto
from django.core.validators import MaxValueValidator, RegexValidator


class PesquisaProdutoForm(forms.Form):

    nome = forms.CharField(
        widget=forms.TextInput(attrs={
                               'class': 'form-control mr-0', 'placeholder': 'Pesquisar', 'aria-label': 'Pesquisar'}),
        required=False,
    )


class PesquisaPorCodigoForm(forms.Form):

    codigo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mr-0',
                                      'placeholder': 'Código do Produto', 'aria-label': 'Digite o Código do Produto'}),
        required=True,
        max_length=20,
    )


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ("codigo", "nome", "categoria", "marca", "imagem", "disponivel", "preco", "altura", "largura",
                  "profundidade", "unidadesPorCaixa", "unidadeDeVenda", "multiploDeVenda", "descricao")
        localized_fields = ("preco", "mutiploDeVenda")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].error_messages = {'required': 'Campo obrigatório.',
                                              'unique': 'Código de produto duplicado.'}
        self.fields['codigo'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputNomeProduto', 'placeholder': 'Nome do Produto'})
        self.fields['codigo'].widget.attrs['readonly'] = True

        self.fields['nome'].error_messages = {'required': 'Campo obrigatório.',
                                              'unique': 'Nome de produto duplicado.'}
        self.fields['nome'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputNomeProduto', 'placeholder': 'Nome do Produto'})

        self.fields['categoria'].error_messages = {
            'required': 'Campo obrigatório'}
        self.fields['categoria'].queryset = Categoria.objects.all().order_by(
            'nome')
        self.fields['categoria'].empty_label = '--- Selecione uma categoria ---'
        self.fields['categoria'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputCategoria'})

        self.fields['marca'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['marca'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputMarca', 'placeholder': 'Marca do Produto'})

        self.fields['imagem'].error_messages = {
            'required': 'Campo obrigatório'}
        self.fields['imagem'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputImagem', 'placeholder': 'Nome do Arquivo de Imagem'})
        self.fields['imagem'].required = False


        self.fields['disponivel'].widget.attrs.update({'class':'custom-control-input'})

        self.fields['preco'].min_value = 0
        self.fields['preco'].error_messages = {'required': 'Campo obrigatório.',
                                               'invalid': 'Valor inválido.',
                                               'max_digits': 'Mais de 5 dígitos no total.',
                                               'max_decimal_places': 'Mais de 2 dígitos decimais.',
                                               'max_whole_digits': 'Mais de 3 dígitos inteiros.'}
        self.fields['preco'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputPreco',
            'placeholder': 'Preço',
            'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'
        })

        self.fields['altura'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['altura'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputAltura', 'placeholder': 'Altura do Produto'})

        self.fields['largura'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['largura'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputLargura', 'placeholder': 'Largura do Produto'})

        self.fields['profundidade'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['profundidade'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputProfundidade', 'placeholder': 'Profundidade do Produto'})


        self.fields['unidadesPorCaixa'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['unidadesPorCaixa'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputUnidadesPorCaixa', 'placeholder': 'Unidades por Caixa do Produto'})

        self.fields['unidadeDeVenda'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['unidadeDeVenda'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputUnidadeDeVenda', 'placeholder': 'Unidade de Venda do Produto'})

        self.fields['multiploDeVenda'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['multiploDeVenda'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputMultiploDeVenda', 'placeholder': 'Multiplo de Venda do Produto'})
        
        self.fields['descricao'].error_messages = {
            'required': 'Campo obrigatório'}
        self.fields['descricao'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inputDescricao'})


class ProdutoCategoriaForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ("categoria",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['categoria'].empty_label = '--- Selecione uma categoria ---'
        self.fields['categoria'].widget.attrs.update(
            {'class': 'mx-auto'})


class QuantidadeForm(forms.Form):
    def __init__(self, *args, **kwargs):

        step = kwargs.pop('multiploDeVenda')
        super(QuantidadeForm, self).__init__(*args, **kwargs)
        self.fields['quantidade'].widget.attrs.update(
            {'data-step': step, 'value': step, 'min': step})
        self.fields['quantidade'].widget.attrs['readonly'] = True

    quantidade = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'qauntidade1', 'type': "text", 'max': "9999", 'class': 'form-control',
                                      'placeholder': 'Digite o Código do Produto', 'aria-label': 'Digite o Código do Produto'}),
        required=True,
        max_length=20,
    )
