# Generated by Django 5.1.10 on 2025-06-10 11:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0006_compra_email_compra_nombre_completo_compra_telefono_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.PositiveSmallIntegerField(choices=[(1, 'administrador'), (3, 'cliente'), (2, 'vendedor'), (4, 'creador')], default=1),
        ),
        migrations.CreateModel(
            name='Creador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
