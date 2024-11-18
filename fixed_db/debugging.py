import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction, IntegrityError
from django.apps import apps

class Command(BaseCommand):
    help = 'Debug loaddata and check for FOREIGN KEY constraint issues'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the fixture file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        try:
            with transaction.atomic():
                call_command('loaddata', file_path)
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR("FOREIGN KEY constraint failed"))
            self.stdout.write(f"Error: {e}")

            # JSON 파일의 데이터를 로드
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.stdout.write("\n--- Debugging Info ---")
            for idx, obj in enumerate(data):
                model = obj.get("model")
                pk = obj.get("pk")
                fields = obj.get("fields")
                self.stdout.write(f"Entry {idx + 1}: Model: {model}, PK: {pk}, Fields: {fields}")

                # Foreign Key fields를 체크
                for field, value in fields.items():
                    if isinstance(value, int):  # 외래 키 값은 일반적으로 정수
                        self.stdout.write(f"    Checking ForeignKey field: {field}, value: {value}")
                        try:
                            app_label, model_name = model.split('.')
                            related_model = apps.get_model(app_label, model_name)
                            if not related_model.objects.filter(pk=value).exists():
                                self.stdout.write(self.style.WARNING(
                                    f"    ForeignKey constraint issue: Model {model} references non-existent PK {value}"
                                ))
                        except Exception as rel_err:
                            self.stdout.write(self.style.ERROR(
                                f"    Error while checking related model: {rel_err}"
                            ))

            self.stdout.write("\nCheck your data file for integrity issues.")
