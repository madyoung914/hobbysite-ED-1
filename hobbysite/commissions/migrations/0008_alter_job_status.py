# Generated by Django 5.1.6 on 2025-05-03 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0007_alter_job_commission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Full', 'Full')], default='Open', max_length=255),
        ),
    ]
