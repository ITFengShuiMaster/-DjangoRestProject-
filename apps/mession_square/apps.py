from django.apps import AppConfig


class MessionSquareConfig(AppConfig):
    name = 'mession_square'

    def ready(self):
        import mession_square.signals
