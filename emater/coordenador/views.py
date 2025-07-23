from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import ProdutorForm, TerrenoForm, TalhaoForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Coordenador, Produtor, Terreno, Talhao
from sistema.utils import is_coordenador_or_superuser
from django.contrib import messages

def index(request):
    return render(request,'sistema/welcome.html')

@login_required
def listaProd(request):
    produtores = Produtor.objects.all()
    coordenador = Coordenador.objects.get(user=request.user)

    contexto = {
        "produtores": produtores,
        'coordenador': coordenador
    }

    return render(request,"coordenador/listaProdutores.html",contexto)


@login_required
def criarProdutor(request): 

    if request.method == "POST":
        form = ProdutorForm(request.POST)
        if form.is_valid():
            produtor = form.save(commit=False)
            produtor.coordenador = Coordenador.objects.get(user=request.user)
            produtor.cidade = request.POST.get('cidade')
            produtor.save()
            messages.success(request, "Produtor cadastrado com sucesso!")
            return redirect('coordenador:Lista_Produtores')
            # redirecionar ou mostrar mensagem de sucesso
    else:
        form = ProdutorForm()
        
    return render(request, 'coordenador/adicionarProdutor.html', {'form': form})

@login_required
def produtor_atualiza(request, id):
    produtor = get_object_or_404(Produtor, id=id)

    if not is_coordenador_or_superuser(request.user, produtor):
        return HttpResponseForbidden("Apenas coordenadores podem acessar esse link.")

    if request.method == "POST":
        form = ProdutorForm(request.POST, instance=produtor)
        if form.is_valid():
            produtor_atualizado = form.save(commit=False)
            produtor.cidade = request.POST.get('cidade')
            produtor_atualizado.save()
            messages.success(request, "Produtor salvo!")
            return redirect('coordenador:Lista_Produtores')
        else:
            messages.error(request, "Erro ao salvar. Verifique os campos!")
    else:
        form = ProdutorForm(instance=produtor)

    return render(request, 'coordenador/produtor-atualiza.html', {
        'form': form,
        'produtor': produtor,
    })


@login_required
def produtor_exclui(request, id):
    produtor = get_object_or_404(Produtor, id=id)

    if not is_coordenador_or_superuser(request.user, produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")

    if request.method == "GET":
        produtor.delete()
        messages.success(request, "Produtor excluído!")
        return redirect('coordenador:Lista_Produtores')
    
@login_required
def produtor_detalhe(request, id):
    produtor = get_object_or_404(Produtor, id=id)

    if not is_coordenador_or_superuser(request.user, produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")
    
    terrenos = Terreno.objects.filter(produtor=produtor).order_by('nome')

    return render(request, 'coordenador/produtor-detalhe.html', {
        'produtor': produtor,
        'terrenos': terrenos
    })


@login_required
def terreno_cria(request, id):
    produtor = get_object_or_404(Produtor, id=id)

    if not is_coordenador_or_superuser(request.user, produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")

    if request.method == "POST":
        print("Entrou no POST")
        form = TerrenoForm(request.POST)

        if form.is_valid():
            terreno = form.save(commit=False)
            terreno.produtor = produtor
            terreno.cidade = request.POST.get('cidade')
            terreno.save()
            messages.success(request, "Terreno criado com sucesso!")
            return redirect('coordenador:produtor_detalhe', id=produtor.id)
    else:
        form = TerrenoForm()

    return render(request, 'coordenador/terreno-cria.html', {'form': form, 'produtor': produtor})

@login_required
def terreno_detalhe(request, id):
    terreno = get_object_or_404(Terreno, id=id)
    
    if not is_coordenador_or_superuser(request.user, terreno.produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")

    talhoes = Talhao.objects.filter(terreno=terreno).order_by('nome')

    return render(request, 'coordenador/terreno-detalhe.html', {'terreno':terreno, 'talhoes':talhoes})

@login_required
def terreno_atualiza(request, id):
    terreno = get_object_or_404(Terreno, id=id)

    if not is_coordenador_or_superuser(request.user, terreno.produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")
    
    if request.method == "POST":
        form = TerrenoForm(request.POST, instance=terreno)
        if form.is_valid():
            terreno_atualizado = form.save(commit=False)
            terreno.cidade = request.POST.get('cidade')
            terreno_atualizado.save()
            messages.success(request, "Terreno salvo!")
            return redirect('coordenador:terreno_detalhe', id=terreno.id)
        else:
            messages.error(request, "Erro ao salvar. Verifique os campos!")
    else:
        form = TerrenoForm(instance=terreno)

    return render(request, 'coordenador/terreno-atualiza.html', {
        'form': form,
        'terreno': terreno,
    })

@login_required
def terreno_exclui(request, id):
    terreno = get_object_or_404(Terreno, id=id)

    if not is_coordenador_or_superuser(request.user, terreno.produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")

    if request.method == "GET":
        terreno.delete()
        messages.success(request, "Terreno excluído!")
        return redirect('coordenador:produtor_detalhe', id=terreno.produtor.id)
    
@login_required
def talhao_cria(request, id):
    terreno = get_object_or_404(Terreno, id=id)

    if not is_coordenador_or_superuser(request.user, terreno.produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")

    if request.method == "POST":
        print("Entrou no POST")
        form = TalhaoForm(request.POST)

        if form.is_valid():
            talhao = form.save(commit=False)
            talhao.terreno = terreno
            talhao.cidade = request.POST.get('cidade')
            talhao.save()
            messages.success(request, "Terreno criado com sucesso!")
            return redirect('coordenador:terreno_detalhe', id=terreno.id)
    else:
        form = TalhaoForm()

    return render(request, 'coordenador/talhao-cria.html', {'form': form, 'terreno': terreno})

@login_required
def talhao_detalhe(request, id):
    talhao = get_object_or_404(Talhao, id=id)
    
    if not is_coordenador_or_superuser(request.user, talhao.terreno.produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")

    return render(request, 'coordenador/talhao-detalhe.html', {'talhao':talhao})

@login_required
def talhao_atualiza(request, id):
    talhao = get_object_or_404(Talhao, id=id)

    if not is_coordenador_or_superuser(request.user, talhao.terreno.produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")
    
    if request.method == "POST":
        form = TalhaoForm(request.POST, instance=talhao)
        if form.is_valid():
            talhao_atualizado = form.save(commit=False)
            talhao.cidade = request.POST.get('cidade')
            talhao_atualizado.save()
            messages.success(request, "Talhão salvo!")
            return redirect('coordenador:talhao_detalhe', id=talhao.id)
        else:
            messages.error(request, "Erro ao salvar. Verifique os campos!")
    else:
        form = TalhaoForm(instance=talhao)

    return render(request, 'coordenador/talhao-atualiza.html', {
        'form': form,
        'talhao': talhao,
    })