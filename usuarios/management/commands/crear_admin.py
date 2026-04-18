from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea un usuario administrador por defecto'

    def handle(self, *args, **options):
        if not Usuario.objects.filter(es_admin=True).exists():
            usuario = Usuario(username='admin', es_admin=True)
            usuario.set_password('1234')
            usuario.save()
            self.stdout.write(self.style.SUCCESS('✅ Usuario admin creado: admin / 1234'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Ya existe un usuario administrador'))