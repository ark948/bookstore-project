from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = "Remvoe records from the given model name."

    def add_arguments(self, parser):
        parser.add_argument(
            'model_name',
            type=str,
            help='Model name to select (case-insensitive, e.g. "User" or "Book").'
        )
        parser.add_argument(
            '--app',
            type=str,
            default=None,
            help='Optional app label if there are models with the same name.'
        )

    def handle(self, *args, **options):
        model_name = options['model_name']
        app_label = options['app']

        try:
            if app_label:
                model = apps.get_model(app_label, model_name)
            else:
                # Try to find by model name only
                # if model was not found, model will equal None
                model = next((m for m in apps.get_models() if m.__name__.lower() == model_name.lower()),
                    None
                )
                if model is None:
                    raise LookupError(f"Model {model_name} was not found.")
            
            records_count = model.objects.count()
            if records_count > 0:
                confirm = input(f"Confirm deletion of {records_count} records in this model ({model._meta.label})? \n[CAUTION: Related records from other tables WILL also be deleted] \n (y/N): ")
                if confirm.lower() in ('y', 'yes'):
                    print("Performing delete...")
                    queryset = model.objects.all().delete()
                else:
                    self.stdout.write(self.style.WARNING('Operation cancelled'))
                    return None

                self.stdout.write(self.style.SUCCESS(
                    f"{queryset[0]} Records were deleted successfully for {model._meta.label}"
                ))
            else:
                self.stdout.write(self.style.ERROR('This table is empty.'))
                return None

        except LookupError as e:
            raise CommandError(f"CommandError: {e}")
        except Exception as e:
            raise CommandError(f"Error: {e}")
