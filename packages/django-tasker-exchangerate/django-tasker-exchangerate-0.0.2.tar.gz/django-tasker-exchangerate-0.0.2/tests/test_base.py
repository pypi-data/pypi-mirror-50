from django.test import TestCase
from django.core.management import call_command
from django_tasker_exchangerate import models


class ExchangeRate(TestCase):
    def test_download(self):
        call_command('exchangerate', '--action=cbrf')
        result = models.ExchangeRate.objects.get(last=True, code='USD', source=1)
        self.assertEqual(result.code, 'USD')
        self.assertIsNotNone(result.value)

        self.assertRegex(str(result.value), r'^[0-9]{2}\.[0-9]{4}$')
        self.assertEqual(result.source, 1)
        self.assertRegex(str(result.date), r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$')
        self.assertEqual(result.get_source_display(), 'Central Bank of Russia')
