from django.core.management.base import BaseCommand

from LBTask.population import fill_database


class Command(BaseCommand):
    help = """
Populates database with random documents. Adds three users with usernames: 'admin', 'manager', 'inspector' and 'guest'.
All of them have password '12345'.
Accept optional argument: 'number'.
    """

    def add_arguments(self, parser):
        parser.add_argument('--number', dest='number', type=int, help='Number of documents to create')

    def handle(self, *args, **options):
        number = 100
        if 'number' in options and options['number'] is not None:
            number = options['number']
        res = fill_database(number)
        self.stdout.write(self.style.SUCCESS('Number of created documents: {0}'.format(res)))
