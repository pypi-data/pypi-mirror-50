from django.core.management.base import BaseCommand
from ... import exchangerate


class Command(BaseCommand):
    help = 'Download currency rates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            nargs='?',
            default='cbrf',
            type=str,
            choices=['cbrf'],
            help='Action; cbrf=Loading rates of the Central Bank of the Russian Federation',
        )

        parser.add_argument(
            '--date',
            nargs='?',
            type=str,
            help='Action; date=Date download',
        )

    def handle(self, *args, **options):
        """
            Загружает с сайта центрального банка курсы валют
        """
        if options.get('action') == 'cbrf':
            exchange_cbrf = exchangerate.CBRF()
            exchange_cbrf.download(date=options.get('date'))
