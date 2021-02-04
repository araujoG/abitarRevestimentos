from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from categoria.models import Categoria
import requests

class Produto(models.Model):
    
    codigo = models.CharField(max_length=20, db_index=True, unique=True, primary_key=True)
    nome = models.CharField(max_length=200, db_index = True, unique = False)
    marca = models.CharField(max_length=50, db_index=True, default="")
    imagem = models.CharField(max_length=150, blank = True)
    disponivel = models.BooleanField(default=True, blank = True)
    preco = models.DecimalField(max_digits=5, decimal_places=2, default=3.99)
    altura = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    largura = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    profundidade = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    unidadesPorCaixa = models.DecimalField(max_digits=5, decimal_places=0, default=1, blank=True)
    unidadeDeVenda = models.CharField(max_length=15, default='un', blank = True)
    multiploDeVenda = models.DecimalField(max_digits=5, decimal_places=2, default=1, blank=True)
    descricao = models.TextField(max_length=800, default="",blank = True)
    slug = models.SlugField(max_length=100, default = '',blank = True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        value = self.nome
        if(type(self.multiploDeVenda)==str):
            self.multiploDeVenda = float(self.multiploDeVenda.replace(",", "."))
        self.slug = slugify(value, allow_unicode=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("Produto")
        verbose_name_plural = ("Produtos")
        db_table = 'produto'
        ordering = ('codigo', 'nome',)

    def __str__(self):
        return f"{self.nome} custa {self.preco}"

    def getAbsoluteUrl(self):
        return reverse('produto:paginaProduto', args=[self.codigo, self.slug])

    def getPrecoParcelado(self):
        return ("%.2f" %(float(self.preco)/6)).replace(".",",")
