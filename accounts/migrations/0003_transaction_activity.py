# Generated by Django 4.2.13 on 2024-07-01 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='activity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
