# Generated by Django 2.0.13 on 2019-08-05 13:03

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_xworkflows.models
import sme_pratoaberto_terceirizadas.dados_comuns.models_abstract
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cardapio', '0002_auto_20190805_1003'),
        ('escola', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoInclusaoAlimentacaoNormal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descricao')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', django_xworkflows.models.StateField(max_length=23, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_APROVADO', 'DRE_PEDE_ESCOLA_REVISAR', 'CODAE_APROVADO']))),
            ],
            options={
                'verbose_name': 'Grupo de inclusão de alimentação normal',
                'verbose_name_plural': 'Grupos de inclusão de alimentação normal',
            },
            bases=(django_xworkflows.models.BaseWorkflowEnabled, models.Model, sme_pratoaberto_terceirizadas.dados_comuns.models_abstract.TemIdentificadorExternoAmigavel),
        ),
        migrations.CreateModel(
            name='InclusaoAlimentacaoContinua',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descricao')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('data_inicial', models.DateField(verbose_name='Data inicial')),
                ('data_final', models.DateField(verbose_name='Data final')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('dias_semana', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Segunda'), (1, 'Terça'), (3, 'Quarta'), (2, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo')], default=[], null=True), size=None)),
                ('status', django_xworkflows.models.StateField(max_length=23, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_APROVADO', 'DRE_PEDE_ESCOLA_REVISAR', 'CODAE_APROVADO']))),
                ('outro_motivo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Outro motivo')),
            ],
            options={
                'verbose_name': 'Inclusão de alimentação contínua',
                'verbose_name_plural': 'Inclusões de alimentação contínua',
            },
            bases=(django_xworkflows.models.BaseWorkflowEnabled, sme_pratoaberto_terceirizadas.dados_comuns.models_abstract.TemIdentificadorExternoAmigavel, models.Model),
        ),
        migrations.CreateModel(
            name='InclusaoAlimentacaoNormal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('prioritario', models.BooleanField(default=False)),
                ('outro_motivo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Outro motivo')),
                ('grupo_inclusao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inclusoes_normais', to='inclusao_alimentacao.GrupoInclusaoAlimentacaoNormal')),
            ],
            options={
                'verbose_name': 'Inclusão de alimentação normal',
                'verbose_name_plural': 'Inclusões de alimentação normal',
            },
        ),
        migrations.CreateModel(
            name='MotivoInclusaoContinua',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Motivo de inclusao contínua',
                'verbose_name_plural': 'Motivos de inclusao contínua',
            },
        ),
        migrations.CreateModel(
            name='MotivoInclusaoNormal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Motivo de inclusao normal',
                'verbose_name_plural': 'Motivos de inclusao normais',
            },
        ),
        migrations.CreateModel(
            name='QuantidadePorPeriodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('numero_alunos', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('grupo_inclusao_normal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quantidades_por_periodo', to='inclusao_alimentacao.GrupoInclusaoAlimentacaoNormal')),
                ('inclusao_alimentacao_continua', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quantidades_por_periodo', to='inclusao_alimentacao.InclusaoAlimentacaoContinua')),
                ('periodo_escolar', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='escola.PeriodoEscolar')),
                ('tipos_alimentacao', models.ManyToManyField(to='cardapio.TipoAlimentacao')),
            ],
            options={
                'verbose_name': 'Quantidade por periodo',
                'verbose_name_plural': 'Quantidades por periodo',
            },
        ),
        migrations.AddField(
            model_name='inclusaoalimentacaonormal',
            name='motivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inclusao_alimentacao.MotivoInclusaoNormal'),
        ),
    ]
