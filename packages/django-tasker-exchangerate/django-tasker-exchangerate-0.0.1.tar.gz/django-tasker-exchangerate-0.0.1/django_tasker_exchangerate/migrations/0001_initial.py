from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('code', models.CharField(max_length=3, verbose_name='Currency type')),
                ('value', models.DecimalField(decimal_places=4, max_digits=7, verbose_name='Value')),
                ('change', models.DecimalField(decimal_places=4, max_digits=7, null=True, verbose_name='Change')),
                ('change_percent', models.DecimalField(
                    decimal_places=4, max_digits=7, null=True, verbose_name='Percent change')
                 ),
                ('source', models.SmallIntegerField(
                    choices=[(1, 'Central Bank of Russia'), (2, 'European Central Bank')], verbose_name='Source')),
                ('last', models.BooleanField(default=False, verbose_name='Last')),
            ],
            options={
                'verbose_name': 'Exchange rate',
                'verbose_name_plural': 'Exchange rate',
                'unique_together': {('date', 'code')},
            },
        ),
    ]
