from django.db import migrations, models


def backfill_year_month(apps, schema_editor):
    """Существующие строки были добавлены до введения year/month, когда
    начисление было жёстко привязано к 2026-07 (см. старые константы
    NACH_YEAR/NACH_MONTH в onceIntNachCharge.py)."""
    YhlasIyul2026InternetNach = apps.get_model('telekom', 'YhlasIyul2026InternetNach')
    YhlasIyul2026InternetNach.objects.filter(year='').update(year='2026', month='07')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('telekom', '0104_nachwithcomment_belet'),
    ]

    operations = [
        migrations.AddField(
            model_name='yhlasiyul2026internetnach',
            name='year',
            field=models.CharField(blank=True, max_length=4, verbose_name='Год начисления'),
        ),
        migrations.AddField(
            model_name='yhlasiyul2026internetnach',
            name='month',
            field=models.CharField(blank=True, max_length=2, verbose_name='Месяц начисления'),
        ),
        migrations.RunPython(backfill_year_month, noop),
    ]
