# Generated by Django 5.1.3 on 2024-12-17 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_rename_profile_badge_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='user',
        ),
        migrations.AddField(
            model_name='badge',
            name='profile',
            field=models.ManyToManyField(blank=True, null=True, related_name='badge', to='main.profile'),
        ),
    ]
