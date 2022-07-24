from django.apps import AppConfig


class BankaccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BankAccount'

    def ready(self):
        import BankAccount.signals


	