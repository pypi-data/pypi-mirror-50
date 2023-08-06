from django.db import models
from django.utils.translation import gettext_lazy as _


class ExchangeRate(models.Model):
    BANK = (
        (1, _('Central Bank of Russia')),
        (2, _('European Central Bank')),
    )

    date = models.DateField(verbose_name=_("Date"))
    code = models.CharField(max_length=3, verbose_name=_("Currency type"))
    value = models.DecimalField(max_digits=7, decimal_places=4, verbose_name=_("Value"))
    change = models.DecimalField(max_digits=7, decimal_places=4, null=True, verbose_name=_("Change"))
    change_percent = models.DecimalField(max_digits=7, decimal_places=4, null=True, verbose_name=_("Percent change"))
    source = models.SmallIntegerField(choices=BANK, verbose_name=_("Source"))
    last = models.BooleanField(default=False, verbose_name=_("Last"))

    class Meta:
        unique_together = (("date", "code"),)
        verbose_name = _("Exchange rate")
        verbose_name_plural = _("Exchange rate")

    def __str__(self):
        return '{code} - {value}'.format(code=self.code, value=self.value)
