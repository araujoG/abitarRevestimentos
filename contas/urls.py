from django.http import request
from django.urls import path

from categoria import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
app_name = 'contas'
# path('', views.listaProduto, name="listaProduto"),

urlpatterns = [
    path('login2/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomAuthenticationForm(request))),]