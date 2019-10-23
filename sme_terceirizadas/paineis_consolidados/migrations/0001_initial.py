# Generated by Django 2.2.6 on 2019-10-23 13:23

import environ
from django.db import migrations, models

import sme_terceirizadas.dados_comuns.behaviors

ROOT_DIR = environ.Path(__file__) - 2

sql_path = ROOT_DIR.path('sql', '0001_solicitacoes.sql')
with open(sql_path, 'r') as f:
    sql = f.read()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(sql),
        migrations.CreateModel(
            name='SolicitacoesCODAE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('escola_uuid', models.UUIDField(editable=False)),
                ('lote', models.CharField(max_length=50)),
                ('dre_uuid', models.UUIDField(editable=False)),
                ('dre_nome', models.CharField(max_length=200)),
                ('terceirizada_uuid', models.UUIDField(editable=False)),
                ('criado_em', models.DateTimeField()),
                ('data_doc', models.DateField()),
                ('tipo_doc', models.CharField(max_length=30)),
                ('desc_doc', models.CharField(max_length=50)),
                ('status_evento', models.PositiveSmallIntegerField()),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'solicitacoes_consolidadas',
                'abstract': False,
                'managed': False,
            },
            bases=(models.Model, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade),
        ),
        migrations.CreateModel(
            name='SolicitacoesDRE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('escola_uuid', models.UUIDField(editable=False)),
                ('lote', models.CharField(max_length=50)),
                ('dre_uuid', models.UUIDField(editable=False)),
                ('dre_nome', models.CharField(max_length=200)),
                ('terceirizada_uuid', models.UUIDField(editable=False)),
                ('criado_em', models.DateTimeField()),
                ('data_doc', models.DateField()),
                ('tipo_doc', models.CharField(max_length=30)),
                ('desc_doc', models.CharField(max_length=50)),
                ('status_evento', models.PositiveSmallIntegerField()),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'solicitacoes_consolidadas',
                'abstract': False,
                'managed': False,
            },
            bases=(models.Model, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade),
        ),
        migrations.CreateModel(
            name='SolicitacoesEscola',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('escola_uuid', models.UUIDField(editable=False)),
                ('lote', models.CharField(max_length=50)),
                ('dre_uuid', models.UUIDField(editable=False)),
                ('dre_nome', models.CharField(max_length=200)),
                ('terceirizada_uuid', models.UUIDField(editable=False)),
                ('criado_em', models.DateTimeField()),
                ('data_doc', models.DateField()),
                ('tipo_doc', models.CharField(max_length=30)),
                ('desc_doc', models.CharField(max_length=50)),
                ('status_evento', models.PositiveSmallIntegerField()),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'solicitacoes_consolidadas',
                'abstract': False,
                'managed': False,
            },
            bases=(models.Model, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade),
        ),
        migrations.CreateModel(
            name='SolicitacoesTerceirizada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('escola_uuid', models.UUIDField(editable=False)),
                ('lote', models.CharField(max_length=50)),
                ('dre_uuid', models.UUIDField(editable=False)),
                ('dre_nome', models.CharField(max_length=200)),
                ('terceirizada_uuid', models.UUIDField(editable=False)),
                ('criado_em', models.DateTimeField()),
                ('data_doc', models.DateField()),
                ('tipo_doc', models.CharField(max_length=30)),
                ('desc_doc', models.CharField(max_length=50)),
                ('status_evento', models.PositiveSmallIntegerField()),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'solicitacoes_consolidadas',
                'abstract': False,
                'managed': False,
            },
            bases=(models.Model, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade),
        ),
    ]
