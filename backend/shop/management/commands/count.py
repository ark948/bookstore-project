from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = "Count the number of records from the given model name."

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
            
            queryset = model.objects.all()
            count = queryset.count()

            self.stdout.write(self.style.SUCCESS(
                f"Records count for {model._meta.label}: {count}"
            ))

        except LookupError as e:
            raise CommandError(f"CommandError: {e}")
        except Exception as e:
            raise CommandError(f"Error: {e}")
