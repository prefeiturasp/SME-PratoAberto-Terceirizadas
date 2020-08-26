# Generated by Django 2.2.13 on 2020-08-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0019_auto_20200826_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsolicitacoesusuario',
            name='solicitacao_tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Solicitação de kit lanche avulsa'), (1, 'Alteração de cardápio'), (2, 'Suspensão de cardápio'), (3, 'Inversão de cardápio'), (4, 'Inclusão de alimentação normal'), (5, 'Inclusão de alimentação da CEI'), (6, 'Suspensão de alimentação da CEI'), (7, 'Inclusão de alimentação contínua'), (8, 'Dieta Especial'), (9, 'Solicitação de kit lanche unificada'), (10, 'Homologação de Produto'), (11, 'Reclamação de Produto'), (31, 'Responde Análise Sensorial')]),
        ),
        migrations.AlterField(
            model_name='logsolicitacoesusuario',
            name='status_evento',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Solicitação Realizada'), (1, 'CODAE autorizou'), (2, 'Terceirizada tomou ciência'), (3, 'Terceirizada recusou'), (4, 'CODAE negou'), (5, 'CODAE pediu revisão'), (6, 'DRE revisou'), (7, 'DRE validou'), (8, 'DRE pediu revisão'), (9, 'DRE não validou'), (10, 'Escola revisou'), (13, 'Escola cancelou'), (14, 'DRE cancelou'), (11, 'Questionamento pela CODAE'), (12, 'Terceirizada respondeu questionamento'), (15, 'Escola solicitou inativação'), (16, 'CODAE autorizou inativação'), (17, 'CODAE negou inativação'), (18, 'Terceirizada tomou ciência da inativação'), (19, 'Terminada por atingir data de término'), (20, 'Pendente homologação da CODAE'), (21, 'CODAE homologou'), (22, 'CODAE não homologou'), (23, 'CODAE pediu análise sensorial'), (24, 'Terceirizada cancelou homologação'), (29, 'Homologação inativa'), (25, 'CODAE suspendeu o produto'), (26, 'Escola/Nutricionista reclamou do produto'), (27, 'CODAE pediu análise da reclamação'), (28, 'CODAE autorizou reclamação'), (32, 'CODAE recusou reclamação'), (33, 'CODAE questionou terceirizada sobre reclamação'), (34, 'CODAE respondeu ao reclamante da reclamação'), (30, 'Terceirizada respondeu a reclamação'), (31, 'Terceirizada respondeu a análise')]),
        ),
    ]
