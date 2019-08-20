# Generated by Django 2.0.13 on 2019-08-20 14:11

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('kit_lanche', '0007_merge_20190819_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaokitlancheavulsa',
            name='status',
            field=django_xworkflows.models.StateField(max_length=34, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_APROVADO', 'DRE_PEDE_ESCOLA_REVISAR', 'DRE_CANCELA_PEDIDO_ESCOLA', 'CODAE_APROVADO', 'CODAE_CANCELOU_PEDIDO', 'TERCEIRIZADA_TOMA_CIENCIA', 'ESCOLA_PEDE_CANCELAMENTO_48H_ANTES'])),
        ),
        migrations.AlterField(
            model_name='solicitacaokitlancheunificada',
            name='status',
            field=django_xworkflows.models.StateField(max_length=23, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaDiretoriaRegionalWorkflow', states=['RASCUNHO', 'CODAE_A_VALIDAR', 'DRE_PEDE_ESCOLA_REVISAR', 'CODAE_CANCELOU_PEDIDO', 'CODAE_APROVADO'])),
        ),
    ]
