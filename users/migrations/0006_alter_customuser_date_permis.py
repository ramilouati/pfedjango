# Generated by Django 5.0.7 on 2024-09-10 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_date_permis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_permis',
            field=models.DateField(default='2001-01-10'),
        ),
    ]
