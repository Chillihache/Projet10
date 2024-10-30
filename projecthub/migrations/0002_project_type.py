# Generated by Django 5.1.2 on 2024-10-12 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projecthub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('back_end', 'Back-end'), ('front_end', 'Front-end'), ('ios', 'IOS'), ('android', 'Android')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]