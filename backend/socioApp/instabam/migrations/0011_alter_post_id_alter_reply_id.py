# Generated by Django 4.1.3 on 2023-07-31 06:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('instabam', '0010_alter_post_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reply',
            name='id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]