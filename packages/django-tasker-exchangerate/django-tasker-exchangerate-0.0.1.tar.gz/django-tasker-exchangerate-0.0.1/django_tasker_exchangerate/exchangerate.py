import requests

from xml.dom import minidom
from decimal import Decimal
from datetime import datetime, timedelta

from django.db import transaction
from . import models


class CBRF:

    @staticmethod
    def model() -> models.ExchangeRate:
        return models.ExchangeRate

    @staticmethod
    def download(date=None) -> None:
        if date:
            dt = datetime.strptime(date, '%Y-%m-%d')
        else:
            dt = datetime.today() + timedelta(1)

        response = requests.get(
            url='https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'.format(date=dt.strftime("%d/%m/%Y"))
        )
        if response.status_code != 200:
            raise Exception("http status {status}".format(status=response.status_code))

        doc = minidom.parseString(response.text)
        root = doc.getElementsByTagName("ValCurs").pop()
        date = root.getAttribute('Date')

        date = date.split('.')
        date.reverse()
        y, m, d = date
        date = datetime(int(y), int(m), int(d))

        # Check exists
        if models.ExchangeRate.objects.filter(source=1, date=date).exists():
            return

        last_result = models.ExchangeRate.objects.filter(source=1, last=True)

        result = []
        currency = doc.getElementsByTagName("Valute")
        for item in currency:
            value = item.getElementsByTagName("Value").pop()
            charcode = item.getElementsByTagName("CharCode").pop()
            value = str(value.firstChild.data)
            code = str(charcode.firstChild.data)
            value = Decimal(value.replace(',', '.'))

            change = 0
            change_percent = 0
            if last_result.exists():
                last = list(filter(lambda x: x.code == code, last_result)).pop()
                change = value - last.value
                change_percent = value / last.value * 100 - 100

            result.append(
                models.ExchangeRate(
                    source=1,
                    date=date,
                    code=code,
                    value=value,
                    change=change,
                    change_percent=change_percent,
                    last=True,
                )
            )

        with transaction.atomic():
            models.ExchangeRate.objects.filter(last=True).update(last=False)
            models.ExchangeRate.objects.bulk_create(result)
