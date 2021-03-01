from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100, db_index = True, unique = False)
    categoriaPai = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    slug = models.SlugField(max_length=110, default = '',blank = True) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome, allow_unicode=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return self.nome

    def categoriasFilhas(self):
        categorias = Categoria.objects.all()
        aux = []
        for cat in categorias:
            if cat.categoriaPai == self:
                aux.append(cat)
        return aux

    def getAbsoluteUrl(self):
        return reverse('categoria:paginaCategoria', args=[self.codigo, self.slug])