# Generated by Django 2.2.6 on 2019-10-22 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paineis_consolidados', '0010_solicitacoesterceirizada'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SolicitacoesAutorizadasDRE',
        ),
        migrations.DeleteModel(
            name='SolicitacoesPendentesDRE',
        ),
    ]