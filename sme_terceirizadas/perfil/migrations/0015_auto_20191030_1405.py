# Generated by Django 2.2.6 on 2019-10-30 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0014_merge_20191024_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vinculo',
            old_name='tipo_instituicao',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='vinculo',
            old_name='instituicao_id',
            new_name='object_id',
        ),
    ]
