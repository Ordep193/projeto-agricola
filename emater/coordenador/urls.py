from django.urls import path
from . import views

app_name='coordenador'

urlpatterns = [
    path('',views.index,name="index"),


    path('listaProdutor/',views.listaProd,name="Lista_Produtores"),
    # path("detalheProdutor/<int:id>",views.detalheProd,name="Detalhe_Produtor"),
    path("adicionarProdutor/",views.criarProdutor,name="adicionarProdutor"),
    path('atualiza-produtor/<int:id>',views.atualiza_produtor,name="atualiza_produtor"),


]