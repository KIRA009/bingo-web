# Generated by Django 2.1.4 on 2019-01-14 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_invites'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Invites',
            new_name='Invite',
        ),
    ]
