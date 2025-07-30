from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from .forms import ProdutorForm, TerrenoForm, TalhaoForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Coordenador, Produtor, Terreno, Talhao
from sistema.utils import is_coordenador_or_superuser
from django.contrib import messages
from openpyxl import Workbook
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProdutorSerializer

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

@login_required
def talhao_exclui(request, id):
    talhao = get_object_or_404(Talhao, id=id)

    if not is_coordenador_or_superuser(request.user, talhao.terreno.produtor):
        return HttpResponseForbidden("Você não tem autorização para acessar essa página.")

    if request.method == "GET":
        talhao.delete()
        messages.success(request, "Terreno excluído!")
        return redirect('coordenador:terreno_detalhe', id=talhao.terreno.produtor.id)
    
def excelGera(request):
    wb = Workbook()
    
    # Aba principal: Produtores
    ws_produtores = wb.active
    ws_produtores.title = "Produtores"
    ws_produtores.append([
        "Nome", "Telefone", "CPF", "Cidade", 
        "CAF", "Validade CAF", "Coordenador"
    ])

    for produtor in Produtor.objects.select_related("coordenador").all():
        ws_produtores.append([
            produtor.nome,
            produtor.telefone,
            produtor.cpf,
            produtor.cidade,
            produtor.caf,
            produtor.validade_caf.strftime('%d/%m/%Y'),
            produtor.coordenador.user.first_name
        ])

    # Abas separadas para cada terreno
    terrenos = Terreno.objects.select_related("produtor").prefetch_related("talhao_set").all()

    for terreno in terrenos:
        # Nome da aba: limitar a 31 caracteres (limite do Excel)
        aba_nome = f"{terreno.produtor.nome[:10]}_{terreno.nome[:20]}"
        aba_nome = aba_nome[:31]

        ws = wb.create_sheet(title=aba_nome)

        # Cabeçalhos
        ws.append([
            f"Terreno: {terreno.nome}",
        ])
        ws.append([
            "Cidade", "Produtor", "Talhão", "Cidade Talhão", 
            "Data Certificação", "Nº Plantas", "Data Plantio", 
            "Variedade", "Área", "Validade CAF"
        ])

        talhoes = Talhao.objects.filter(terreno=terreno)
        for talhao in talhoes:
            ws.append([
                terreno.cidade,
                terreno.produtor.nome,
                talhao.nome,
                talhao.terreno.cidade,
                talhao.data_certificacao.strftime('%d/%m/%Y'),
                talhao.numero_plantas,
                talhao.data_plantio.strftime('%d/%m/%Y'),
                talhao.variedade,
                talhao.area,
                talhao.validade_caf.strftime('%d/%m/%Y')
            ])

    # Gerar resposta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=relatorio_produtores.xlsx'
    wb.save(response)
    return response

@api_view(['GET'])
def api_enviar_produtor(request, id):
    chave = request.headers.get('X-API-Key')
    if chave != 'segredo123':
        return Response({'erro': 'Acesso não autorizado!'}, status=status.HTTP_401_UNAUTHORIZED)

    produtor = get_object_or_404(Produtor, id=id)
    serializer = ProdutorSerializer(produtor)
    return Response(serializer.data)

