# Generated by Django 5.1.2 on 2024-10-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projecthub', '0009_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
