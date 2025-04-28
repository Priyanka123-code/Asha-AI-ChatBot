# knowledgebase/management/commands/import_events.py
from django.core.management.base import BaseCommand
import csv
from knowledgebase.models import StartupEvent

class Command(BaseCommand):
    help = 'Import events from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    StartupEvent.objects.create(
                        event_name=row['event_name'],
                        event_date=row['event_date'],
                        location=row['location'],
                        description=row['description']
                    )
            self.stdout.write(self.style.SUCCESS('✅ Events imported successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing column in CSV: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))