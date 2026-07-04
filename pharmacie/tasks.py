from background_task import background
from django.core.mail import send_mail
from django.conf import settings
from .models import Medicament, AlerteConfig
from datetime import date

@background(schedule=60)  # S'exécute toutes les 60 secondes
def verifier_et_envoyer_alertes():
    medicaments = Medicament.objects.all()
    for medoc in medicaments:
        try:
            config = AlerteConfig.objects.get(user__is_superuser=True)
        except AlerteConfig.DoesNotExist:
            continue

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
        if medoc.date_peremption:
            jours_restants = (medoc.date_peremption - date.today()).days
            if 0 <= jours_restants <= config.seuil_peremption:
                message = f"⚠️ ALERTE PÉREMPTION : {medoc.nom} expire dans {jours_restants} jours."
                if config.envoyer_email and config.email_alerte:
                    send_mail(
                        "Alerte Péremption - PharmaGest",
                        message,
                        settings.EMAIL_HOST_USER,
                        [config.email_alerte],
                        fail_silently=False,
                    )