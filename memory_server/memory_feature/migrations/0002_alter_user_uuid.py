# Generated by Django 4.2.1 on 2023-06-08 18:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('memory_feature', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('80a4356b-243e-4664-b52f-a38a705286a7'), editable=False, unique=True),
        ),
    ]