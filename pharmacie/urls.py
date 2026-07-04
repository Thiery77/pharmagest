from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_de_bord, name='tableau'),
    path('ajouter/', views.ajouter_medicament, name='ajouter'),
    path('modifier/<int:id>/', views.modifier_medicament, name='modifier'),
    path('supprimer/<int:id>/', views.supprimer_medicament, name='supprimer'),
]