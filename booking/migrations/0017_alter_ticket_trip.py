# Generated by Django 5.2 on 2025-05-21 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_alter_ticket_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='booking.trip'),
        ),
    ]
