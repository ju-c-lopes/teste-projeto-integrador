from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from pi.models import Habilidades, Aula, Docente, Turma

# Create your views here.
def index(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    return render(request, 'index.html') # A modificar string de retorno 

def sobre_nos(request):
    return render(request, 'about-us.html')

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Replace 'home' with your desired URL after successful login
            else:
                error_message = "Usuário inválido."  # Error message for invalid login   
        else:
            error_message = "Preencha o formulário corretamente."  # Error message for invalid form
    else:
        form = LoginForm()
        error_message = None
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def logout_user(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if len(Docente.objects.all()) == 0:
                cont = 0
            else:
                ultimo = Docente.objects.last()
                cont = ultimo.cod_doc
            docente = Docente.objects.create(
                cod_doc = cont + 1,
                nome_doc = request.POST['nome'],
                eventual_doc = request.POST['is_temporary_teacher'],
            )
            docente.save()
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'signup.html', {'form': form})

def cadastrar_aula(request):
    
    codigos = Habilidades.objects.all().values()
    escolhas = None
    if request.method == 'POST':
        escolhas = {
            'cod_hab': request.POST['habilidade'],
            'turma': request.POST['turma'],
            'disciplina': request.POST['disciplina'],
            'descricao': request.POST['descricao'],
        }

    dados = {
        'codigos': [v['cod_hab'] for v in codigos],
        'descricao': [v['desc_habilidade'] for v in codigos],
    }
    if escolhas is not None and escolhas['cod_hab'] != '':
        dados['retorno'] = []
        for v in codigos:
            if v['cod_hab'] == escolhas['cod_hab']:
                escolha = {
                    'cod_hab': v['cod_hab'],
                    'turma': request.POST['turma'],
                    'disciplina': request.POST['disciplina'],
                    'descricao': v['desc_habilidade'],
                }
                dados['retorno'].append(escolha)
    else:
        dados['retorno'] = []
        for v in codigos:
            if escolhas is not None and \
                escolhas['descricao'] != '' and \
                escolhas['descricao'] in v['desc_habilidade']:
                escolha = {
                    'cod_hab': v['cod_hab'],
                    'turma': request.POST['turma'],
                    'disciplina': request.POST['disciplina'],
                    'descricao': v['desc_habilidade'],
                }
                dados['retorno'].append(escolha)
    cont = 0
    # if escolhas is not None and escolhas['cod_hab'] != '':
    #     cont = 1
    if escolhas is not None and len(dados['retorno']) >= 1:
        cont = len(dados['retorno'])
    dados['cont'] = cont
    return render(request, 'listagens.html', dados)

def mais_info(request):
    infos = {
        'cod_hab': request.GET['cod_hab'],
        'turma': request.GET['turma'],
        'disciplina': request.GET['disciplina'],
        'descricao': request.GET['descricao'],
    }
    # print(infos)
    return render(request, 'mais-info.html', infos)

def salvar_aula(request):
    # print(request.POST)
    # print(request.user.nome)
    turmas = {'primeiro ano': '1° Ano', 'segundo ano': '2° Ano', 'terceiro ano': '3° Ano'}
    turma = turmas[request.POST['turma']]
    # print(turma, type(turma))
    lista_turmas = Turma.objects.get(nome_turma=turma).cod_turma

    docente = Docente.objects.get(nome_doc=request.user.nome)
    # print(Aula.objects.last())
    if Aula.objects.last() is None:
        cont = 1
    else:
        cont = Aula.objects.last().cod_aula + 1
    print(cont)

    aula = Aula.objects.create(
        cod_aula = cont,
        cod_hab = Habilidades.objects.get(cod_hab=request.POST['cod_hab']),
        disciplina = request.POST['disciplina'],
        desc_aula = request.POST['descricao'],
        cod_doc = Docente.objects.get(cod_doc=docente.cod_doc),
        cod_turma = Turma.objects.get(cod_turma=lista_turmas),
        fluxo_aula = request.POST['fluxo'],
        info_adicionais = request.POST['adicionais']
    )
    aula.save()
    # falta apenas saber onde serão salvas as informacões que será executada neste processo
    return render(request, 'aula-salva.html')