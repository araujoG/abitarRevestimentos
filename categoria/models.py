from django.db import models
from django.urls import reverse

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100, db_index = True, unique = False)
    categoriaPai = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None, blank=True)    

    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return self.nome

