from django.core.management.base import BaseCommand
from base.models import TestCode, Test
import csv
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Import student data from CSV and generate test codes'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('test_id', type=int, help='ID of the test to generate codes for')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        test_id = options['test_id']
        
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Test with ID {test_id} does not exist'))
            return

        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate unique code
                code = TestCode.generate_code()
                
                # Create test code
                TestCode.objects.create(
                    test=test,
                    student_name=row['Name'],   # Capital N
                    student_email=row['Email'], # Capital E
                    code=code,
                    expires_at=timezone.now() + timedelta(hours=24)
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created code {code} for {row["Name"]} ({row["Email"]})'
                    )
                ) 