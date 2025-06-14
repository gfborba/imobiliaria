from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def cadastro_cliente(request):
    if request.method == "POST":
        try:
            cliente = Cliente.objects.create(
                nome=request.POST.get('nome'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone'),
                cpf=request.POST.get('cpf'),
                endereco=request.POST.get('endereco'),
                corretor=request.user
            )
            return redirect('index')
        except Exception as e:
            return render(request, 'pages/cadastro.html', {'error': 'Erro ao cadastrar cliente. Verifique se o email ou CPF já não estão cadastrados.'})
    
    return render(request, 'pages/cadastro.html')
