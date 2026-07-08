from django.db import models
from django.contrib.auth.models import User

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
    
class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
    
class Commande(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    date_commande = models.DateTimeField(auto_now_add=True)
    date_livraison = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('en_attente', 'En attente'),
            ('livre', 'Livré'),
            ('annule', 'Annulé'),
        ],
        default='en_attente'
    )

    def __str__(self):
        return f"{self.medicament.nom} - {self.fournisseur.nom}"