# Generated by Django 5.1.6 on 2025-03-02 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='num_choices',
            field=models.IntegerField(default=4, help_text='Number of choices for this question'),
        ),
    ]
