from django.db import models

class Medicament(models.Model):
    nom = models.CharField(max_length=255)
    code_barres = models.CharField(max_length=255, blank=True, null=True)
    fournisseur = models.CharField(max_length=255, blank=True, null=True)
    quantite = models.IntegerField(default=0)
    date_peremption = models.DateField(blank=True, null=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    seuil_alerte = models.IntegerField(default=5)
    emplacement = models.CharField(max_length=100, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
from django.db import models
from django.contrib.auth.models import User

class AlerteConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_alerte = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)  # format +225...
    seuil_stock = models.IntegerField(default=5)  # alerte quand stock < ce seuil
    seuil_peremption = models.IntegerField(default=30)  # alerte quand péremption < ce seuil
    envoyer_email = models.BooleanField(default=True)
    envoyer_sms = models.BooleanField(default=False)

    def __str__(self):
        return f"Alertes de {self.user.username}"