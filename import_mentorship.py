from django.core.management.base import BaseCommand
import csv
from knowledgebase.models import MentorshipOpportunity

class Command(BaseCommand):
    help = 'Import mentorship opportunities from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    MentorshipOpportunity.objects.create(
                        mentor_name=row['mentor_name'],
                        expertise_area=row['expertise_area'],
                        available_slots=int(row['available_slots']),
                        description=row['description']
                    )
            self.stdout.write(self.style.SUCCESS('✅ Mentorships imported successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing column in CSV: {e}'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Invalid value for available_slots: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))