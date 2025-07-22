from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import ProdutorForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Coordenador, Produtor
from sistema.utils import is_coordenador_or_superuser
from django.contrib import messages

def index(request):
    return render(request,'sistema/welcome.html')

def listaProd(request):
    produtres = Produtor.objects.all()
    coordenador = Coordenador.objects.get(user=request.user)

    contexto = {
        "produtores": produtres,
        'coordenador': coordenador
    }

    return render(request,"coordenador/listaProdutores.html",contexto)

# def criarProdutor(request):
#     if not is_coordenador_or_superuser(request.user):
#         return HttpResponseForbidden("Apenas os coordenadores podem acessar esse link.")
    
#     if request.method == "POST":
#         coordenador = Coordenador.objects.get(user=request.user)
        
#         produtor = Produtor(
#             telefone = request.POST.get('telefone'),
#             terreno = request.POST.get('terreno'),
#             email = request.POST.get('email'),
#             nome = request.POST.get('nome'),
#             cpf = request.POST.get('cpf'),
#             cidade = request.POST.get('cidade'),
#             estado = request.POST.get('estado'),
#             endereco = request.POST.get('endereco'),
#             caf = request.POST.get('caf'),
#             validade_caf = request.POST.get('Vcaf'),
#             coordenador = coordenador,
#         )

#         produtor.save()



@login_required
def criarProdutor(request):
    if not is_coordenador_or_superuser(request.user):
        return HttpResponseForbidden("Apenas os coordenadores podem acessar esse link.")

    if request.method == "POST":
        form = ProdutorForm(request.POST)
        if form.is_valid():
            produtor = form.save(commit=False)
            produtor.coordenador = Coordenador.objects.get(user=request.user)
            produtor.save()
            messages.success(request, "Produtor cadastrado com sucesso!")

            # redirecionar ou mostrar mensagem de sucesso
    else:
        form = ProdutorForm()
        
    return render(request, 'coordenador/listaProdutores.html', {'form': form})

@login_required
def atualiza_produtor(request, id):
    produtor = get_object_or_404(Produtor, id=id)
    
    if not is_coordenador_or_superuser(request.user):
        return HttpResponseForbidden("Apenas coordenadores podem acessar esse link.")
    
    if request.method == "POST":
        form = ProdutorForm(request.POST, instance=produtor)
        if form.is_valid():
           form.save(commit=False)
           messages.success("Produtor salvo!")
           return redirect('produtor:Lista_Produtores')
    else:
        messages.error(request, "Erro ao salvar. Verifique os campos!")

    return render(request, 'coordenador/atualiza-produtor.html', {
        'form': form,
    })

