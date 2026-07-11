import warnings

from django.apps import AppConfig

warnings.filterwarnings(
    'ignore',
    message='Accessing the database during app initialization is discouraged',
    category=RuntimeWarning
)


class ArchivesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'archives'

    def ready(self):
        # Per Django doc, this is OK if the method is idempotent
        try:
            from .models import PairingType
            pairings = PairingType.objects.all()

            if len(pairings) == 0:
                PairingType.objects.create(pairing_type="oth", label="Autre")
                PairingType.objects.create(pairing_type="het", label="Hétéro")
                PairingType.objects.create(pairing_type="mm", label="M/M")
                PairingType.objects.create(pairing_type="ff", label="F/F")
                PairingType.objects.create(pairing_type="gen", label="Aucun")
        except Exception:
            pass