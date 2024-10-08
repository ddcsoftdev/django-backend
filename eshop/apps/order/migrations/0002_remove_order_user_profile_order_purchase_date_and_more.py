# Generated by Django 5.1 on 2024-08-20 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('user', '0007_remove_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='order',
            name='purchase_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='user.userprofile'),
        ),
    ]
