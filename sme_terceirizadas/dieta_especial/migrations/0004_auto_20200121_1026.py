# Generated by Django 2.2.8 on 2020-01-21 13:26

import django_xworkflows.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dieta_especial', '0003_auto_20200116_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaodietaespecial',
            name='status',
            field=django_xworkflows.models.StateField(max_length=26, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='DietaEspecialWorkflow', states=['RASCUNHO', 'CODAE_A_AUTORIZAR', 'CODAE_NEGOU_PEDIDO', 'CODAE_AUTORIZADO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU'])),
        ),
    ]
