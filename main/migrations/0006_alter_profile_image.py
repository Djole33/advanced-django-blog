# Generated by Django 5.1.3 on 2024-12-15 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_blogpost_image_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='images/profile_p/default.png', upload_to='images/profile_p/'),
        ),
    ]