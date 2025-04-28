from django.core.management.base import BaseCommand
import csv
from knowledgebase.models import JobListing
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Imports job listings from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    JobListing.objects.update_or_create(
                        title=row['title'],
                        company=row['company'],
                        defaults={
                            'location': row['location'],
                            'description': row['description'],
                            'posted_at': row['posted_at'] if row['posted_at'] else now().date(),
                        }
                    )
            self.stdout.write(self.style.SUCCESS('✅ Jobs imported successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing column in CSV: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))