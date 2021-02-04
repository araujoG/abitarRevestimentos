from django.shortcuts import render

def index(request):
    frase = "esta é a frase da index Abitar"
    
    return render(request, 'index.html', {})