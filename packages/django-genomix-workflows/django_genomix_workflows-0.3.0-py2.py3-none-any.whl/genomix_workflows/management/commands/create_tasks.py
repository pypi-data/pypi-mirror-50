from django.core.management import BaseCommand

from ... import services


class Command(BaseCommand):
    help = 'Create Tasks in Database'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='Mapping between TestCode and details')
        parser.add_argument(
            '--mode',
            dest='mode',
            choices=['Create', 'Update'],
            default='Create'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        mode = options['mode']
        services.load_tasks(filename=filename, mode=mode)
