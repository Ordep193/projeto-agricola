from django.urls import path
from . import views

app_name='coordenador'

urlpatterns = [
    path('',views.index,name="index"),
    path('listaProdutor/',views.listaProd,name="Lista_Produtores"),
    path("produtor-detalhe/<int:id>",views.produtor_detalhe,name="produtor_detalhe"),
    path("adicionarProdutor/",views.criarProdutor,name="adicionarProdutor"),
    path('produtor-atualiza/<int:id>',views.produtor_atualiza,name="produtor_atualiza"),
    path('produtor-exclui/<int:id>', views.produtor_exclui, name='produtor_exclui'),
    path('terreno-cria/<int:id>', views.terreno_cria, name="terreno_cria"),
    path('terreno-detalhe/<int:id>', views.terreno_detalhe, name="terreno_detalhe"),
    path('terreno-atualiza/<int:id>', views.terreno_atualiza, name="terreno_atualiza"),
    path('terreno-exclui/<int:id>', views.terreno_exclui, name="terreno_exclui"),
    path('talhao-cria/<int:id>', views.talhao_cria, name="talhao_cria"),
    path('talhao-detalhe/<int:id>', views.talhao_detalhe, name="talhao_detalhe"),
    path('talhao-atualiza/<int:id>', views.talhao_atualiza, name="talhao_atualiza"),
    path('talhao-exclui/<int:id>', views.talhao_exclui, name="talhao_exclui"),
    path('teste_excel',views.excelGera,name="teste_excel"),
    path('api/produtor/<int:id>/', views.api_enviar_produtor, name="api_enviar_produtor"),
]