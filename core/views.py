from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Historico
from .forms import CadastroForm
from django.contrib import messages
import re


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('calculadora')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            # Validação de e-mail com regex
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messages.error(request, 'E-mail inválido.')
                return render(request, 'core/cadastro.html', {'form': form})

            # Validação de senha mínima
            if len(senha) < 5:
                messages.error(request, 'A senha deve ter pelo menos 5 caracteres.')
                return render(request, 'core/cadastro.html', {'form': form})

            User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                email=email,
                password=senha
            )
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'core/cadastro.html', {'form': form})


@login_required(login_url='login')
def calculadora_view(request):
    if request.method == 'POST':
        expressao = request.POST.get('expressao')
        try:
            # Substitui % por /100 para cálculos de porcentagem
            resultado = str(eval(expressao.replace('%', '/100')))
            Historico.objects.create(
                usuario=request.user,
                expressao=expressao,
                resultado=resultado
            )
        except Exception:
            resultado = 'Erro'

        historico = Historico.objects.filter(usuario=request.user).order_by('-data')
        return render(request, 'core/calculadora.html', {
            'resultado': resultado,
            'expressao': expressao,
            'historico': historico
        })

    historico = Historico.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'core/calculadora.html', {
        'resultado': '',
        'expressao': '',
        'historico': historico
    })


@login_required(login_url='login')
def apagar_historico(request):
    Historico.objects.filter(usuario=request.user).delete()
    return redirect('calculadora')