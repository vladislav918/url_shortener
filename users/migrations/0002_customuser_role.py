# Generated by Django 5.1.1 on 2024-09-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('user', 'Пользователь')], default='user', max_length=10),
        ),
    ]
