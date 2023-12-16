from django.core.management import BaseCommand
from django.core.management import call_command
from datetime import datetime

class Command(BaseCommand):
    """
    Комманда для создания резервной копии базы данных
    """
    def handle(self, *args, **options):
        self.stdout.write('Waiting for dump...')
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '--exclude=contenttypes',
            '--exclude=admin.logentry',
            '--ident=4',
            f'--output=database-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json'
        )
        self.stdout.write(self.style.SUCCES('Database successfully backed up'))

