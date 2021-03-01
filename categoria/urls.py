from django.urls import path

from categoria import views

app_name = 'categoria'
# path('', views.listaProduto, name="listaProduto"),

urlpatterns = [
    path('<slug:slug>/', views.paginaCategoria, name="paginaCategoria"),
]