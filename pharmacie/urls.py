from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_de_bord, name='tableau'),
    path('ajouter/', views.ajouter_medicament, name='ajouter'),
    path('modifier/<int:id>/', views.modifier_medicament, name='modifier'),
    path('supprimer/<int:id>/', views.supprimer_medicament, name='supprimer'),
    path('qr/<int:id>/', views.generer_qr_code, name='qr_code'),
    path('exporter-pdf/', views.exporter_pdf, name='exporter_pdf'),
]