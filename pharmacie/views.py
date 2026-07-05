from django.shortcuts import render, redirect
from .models import Medicament
from .forms import MedicamentForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Medicament, AlerteConfig

def verifier_et_envoyer_alertes():
    medicaments = Medicament.objects.all()
    for medoc in medicaments:
        # Récupérer la config de l'utilisateur (pour le moment, on prend le premier superuser)
        try:
            config = AlerteConfig.objects.get(user__is_superuser=True)
        except AlerteConfig.DoesNotExist:
            continue  # pas de config, on saute

        # Vérifier seuil de stock
        if medoc.quantite <= config.seuil_stock:
            message = f"⚠️ ALERTE STOCK : {medoc.nom} n'a plus que {medoc.quantite} unités."
            if config.envoyer_email and config.email_alerte:
                send_mail(
                    "Alerte Stock - PharmaGest",
                    message,
                    settings.EMAIL_HOST_USER,
                    [config.email_alerte],
                    fail_silently=False,
                )
            if config.envoyer_sms and config.telephone:
                # (On ajoutera l'envoi SMS avec Twilio ou Africa's Talking plus tard)
                print(f"[SMS] {message} -> {config.telephone}")

        # Vérifier péremption
        if medoc.date_peremption:
            from datetime import date
            jours_restants = (medoc.date_peremption - date.today()).days
            if 0 <= jours_restants <= config.seuil_peremption:
                message = f"⚠️ ALERTE PÉREMPTION : {medoc.nom} expire dans {jours_restants} jours."
                # Envoyer Email et/ou SMS (même logique que ci-dessus)
                if config.envoyer_email and config.email_alerte:
                    send_mail(
                        "Alerte Péremption - PharmaGest",
                        message,
                        settings.EMAIL_HOST_USER,
                        [config.email_alerte],
                        fail_silently=False,
                    )
                if config.envoyer_sms and config.telephone:
                    print(f"[SMS] {message} -> {config.telephone}")

# Vue pour le tableau de bord
def tableau_de_bord(request):
    # Récupérer tous les médicaments
    medicaments = Medicament.objects.all()
    
    # Si une recherche est faite
    recherche = request.GET.get('recherche')
    if recherche:
        medicaments = medicaments.filter(nom__icontains=recherche)
    
    return render(request, 'tableau.html', {'medicaments': medicaments})
# Vue pour ajouter un médicament
def ajouter_medicament(request):
    if request.method == 'POST':
        print("➡️ On est dans le POST")  # <-- Ajoute ça
        form = MedicamentForm(request.POST)
        if form.is_valid():
            print("✅ Formulaire valide !")
            form.save()
            print("SAUVEGARDE RÉUSSIE")
            return redirect('tableau')
    else:
        form = MedicamentForm()
    return render(request, 'ajouter.html', {'form': form})
# Vue pour modifier un médicament
def modifier_medicament(request, id):
    medicament = Medicament.objects.get(id=id)
    if request.method == 'POST':
        form = MedicamentForm(request.POST, instance=medicament)
        if form.is_valid():
            form.save()
            return redirect('tableau')
    else:
        form = MedicamentForm(instance=medicament)
    return render(request, 'modifier.html', {'form': form})

# Vue pour supprimer un médicament
def supprimer_medicament(request, id):
    medicament = Medicament.objects.get(id=id)
    if request.method == 'POST':
        medicament.delete()
        return redirect('tableau')
    return render(request, 'supprimer.html', {'medicament': medicament})