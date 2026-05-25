from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps


class Command(BaseCommand):
    help = 'Resetea las secuencias de PostgreSQL para todas las tablas'

    def handle(self, *args, **options):
        for model in apps.get_models():
            if not model._meta.pk or model._meta.pk.name != 'id':
                continue
            table = model._meta.db_table
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT setval(pg_get_serial_sequence(%s, 'id'), "
                        "COALESCE((SELECT MAX(id) FROM \"" + table + "\"), 1))",
                        [table]
                    )
                self.stdout.write(self.style.SUCCESS(f'OK  {table}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'SKIP {table}: {e}'))
