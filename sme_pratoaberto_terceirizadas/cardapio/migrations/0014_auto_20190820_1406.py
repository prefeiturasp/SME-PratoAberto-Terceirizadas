# Generated by Django 2.0.13 on 2019-08-20 17:06

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('cardapio', '0013_auto_20190820_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gruposuspensaoalimentacao',
            name='status',
            field=django_xworkflows.models.StateField(max_length=16, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='InformativoPartindoDaEscolaWorkflow', states=['RASCUNHO', 'INFORMADO'])),
        ),
    ]
