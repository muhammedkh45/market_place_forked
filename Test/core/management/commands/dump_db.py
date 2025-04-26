from django.core.management.base import BaseCommand
from django.db import connections
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Dumps the database to SQL format'

    def handle(self, *args, **options):
        # Get the database connection
        connection = connections['default']
        
        # Create a directory for the dump if it doesn't exist
        if not os.path.exists('db_dumps'):
            os.makedirs('db_dumps')
            
        # Create the SQL dump
        with open('db_dumps/database_dump.sql', 'w', encoding='utf-8') as f:
            # Dump the schema
            call_command('sqlmigrate', 'admin', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'auth', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'contenttypes', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'sessions', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'core', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'items', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'deposit', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'carts', '0001_initial', stdout=f)
            call_command('sqlmigrate', 'dashboard', '0001_initial', stdout=f)
            
            # Dump the data
            call_command('dumpdata', format='json', indent=2, stdout=f)
            
        self.stdout.write(self.style.SUCCESS('Successfully created database dump at db_dumps/database_dump.sql')) 