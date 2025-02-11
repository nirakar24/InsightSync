# Generated by Django 5.1.6 on 2025-02-11 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='spending_factor',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Random spending factor (0.5 - 1.5) assigned at creation.', max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
