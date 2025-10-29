from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from shop.models import Order, OrderItem

class Command(BaseCommand):
    help = 'Removes all records in given table.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('table_name', type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        if options['table_name'] in ('orders', 'Orders'):
            try:
                result = Order.objects.all().delete()
            except Exception as error:
                print('ERROR')
                raise CommandError("Some error occurred: %s" % error)
            self.stdout.write( self.style.SUCCESS("Successfully deleted %s records." % result[0]) )
        elif options['table_name'] in ('order_item', 'orderitems'):
            try:
                result = OrderItem.objects.all().delete()
            except Exception as error:
                print('ERROR')
                raise CommandError("Some error occurred: %s" % error)
            self.stdout.write( self.style.SUCCESS("Successfully deleted %s records." % result[0]) )
        else:
            print("Argument failure or table name not recognized.")
    