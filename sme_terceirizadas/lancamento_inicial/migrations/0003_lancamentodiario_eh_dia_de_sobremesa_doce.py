# Generated by Django 2.2.13 on 2020-10-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lancamento_inicial', '0002_lancamentodiario_ref_enteral'),
    ]

    operations = [
        migrations.AddField(
            model_name='lancamentodiario',
            name='eh_dia_de_sobremesa_doce',
            field=models.BooleanField(default=False),
        ),
    ]
