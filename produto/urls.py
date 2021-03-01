from django.urls import path

from produto import views

app_name = 'produto'

urlpatterns = [
    path('', views.listaProduto, name="listaProduto"),
    path('administrar/cadastroPorCodigo/', views.cadastraProdutoPorCodigo, name="cadastraProdutoPorCodigo"),
    path('<slug:codigo>/<slug:slugProduto>/', views.paginaProduto, name="paginaProduto"),
    path('administrar/', views.painelAdmin, name="painelAdminProduto"),
    path('administrar/cadastro', views.cadastraProduto, name='cadastraProduto'),
    path('administrar/buscaBling/<slug:codigo>/', views.buscaProdutoBling, name='buscaProdutoBling'),
    path('administrar/edita/<slug:codigo>/<slug:slugProduto>/', views.editaProduto, name='editaProduto'),
    path('administrar/remove/<slug:codigo>/', views.removeProduto, name='removeProduto'),
    path('administrar/sincrozaPreco/<slug:codigo>/', views.sincronizaPrecoProduto, name='sincronizaPrecoProduto'),
]