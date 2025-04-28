# knowledgebase/management/commands/import_women_empowerment.py
from django.core.management.base import BaseCommand
import csv
from knowledgebase.models import WomenEmpowerment

class Command(BaseCommand):
    help = 'Import women empowerment data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                # Debug: Print the first few lines of the file
                self.stdout.write(self.style.WARNING('File content preview:'))
                for i, line in enumerate(csvfile):
                    self.stdout.write(self.style.WARNING(line.strip()))
                    if i >= 4:  # Print only the first 5 lines
                        break

                csvfile.seek(0)  # Reset file pointer to the beginning
                reader = csv.DictReader(csvfile)

                # Debug: Print detected fieldnames
                self.stdout.write(self.style.WARNING(f'Detected columns: {reader.fieldnames}'))

                # Normalize column names to handle whitespace and case sensitivity
                reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

                # Validate required columns
                required_columns = ['title']
                missing_columns = [col for col in required_columns if col not in reader.fieldnames]
                if missing_columns:
                    self.stdout.write(self.style.ERROR(f'Missing columns in CSV: {missing_columns}'))
                    return

                for row in reader:
                    WomenEmpowerment.objects.update_or_create(
                        title=row['title'],
                        defaults={'description': row.get('description', '')}
                    )
            self.stdout.write(self.style.SUCCESS('✅ Women empowerment data imported successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing column in CSV: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))