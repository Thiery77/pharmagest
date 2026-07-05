from django.shortcuts import render, redirect
from .models import Medicament
from .forms import MedicamentForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Medicament, AlerteConfig
import qrcode
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from django.http import FileResponse
import io
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
    medicaments = Medicament.objects.all()
    recherche = request.GET.get('recherche')
    if recherche:
        medicaments = medicaments.filter(nom__icontains=recherche)
    
    # Ajouter un champ "en_alerte" à chaque médicament
    for m in medicaments:
        m.en_alerte = m.quantite <= m.seuil_alerte
    
    return render(request, 'tableau.html', {'medicaments': medicaments})
    
    # Si une recherche est faite
    recherche = request.GET.get('recherche')
    if recherche:
        medicaments = medicaments.filter(nom__icontains=recherche)
    
    return render(request, 'tableau.html', {'medicaments': medicaments})
# Vue pour ajouter un médicament
@login_required
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
@login_required
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
@login_required
def supprimer_medicament(request, id):
    medicament = Medicament.objects.get(id=id)
    if request.method == 'POST':
        medicament.delete()
        return redirect('tableau')
    return render(request, 'supprimer.html', {'medicament': medicament})

import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse

@login_required
def generer_qr_code(request, id):
    medicament = Medicament.objects.get(id=id)
    data = f"{medicament.nom}\n{medicament.code_barres}"
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")

@login_required
def exporter_pdf(request):
    medicaments = Medicament.objects.all()
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Titre
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30 * mm, height - 30 * mm, "Rapport de stock - PharmaGest")
    
    # En-têtes du tableau
    c.setFont("Helvetica-Bold", 12)
    y = height - 50 * mm
    c.drawString(20 * mm, y, "Nom")
    c.drawString(80 * mm, y, "Code-barres")
    c.drawString(140 * mm, y, "Quantité")
    c.drawString(200 * mm, y, "Prix vente")
    
    # Contenu
    c.setFont("Helvetica", 10)
    y -= 10 * mm
    for m in medicaments:
        c.drawString(20 * mm, y, m.nom)
        c.drawString(80 * mm, y, str(m.code_barres))
        c.drawString(140 * mm, y, str(m.quantite))
        c.drawString(200 * mm, y, f"{m.prix_vente} €")
        y -= 8 * mm
        
        # Nouvelle page si nécessaire
        if y < 20 * mm:
            c.showPage()
            y = height - 30 * mm
            c.setFont("Helvetica-Bold", 12)
            c.drawString(20 * mm, y, "Nom")
            c.drawString(80 * mm, y, "Code-barres")
            c.drawString(140 * mm, y, "Quantité")
            c.drawString(200 * mm, y, "Prix vente")
            c.setFont("Helvetica", 10)
            y -= 10 * mm
    
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="rapport_stock.pdf")

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tableau')
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'form': form})