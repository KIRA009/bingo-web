# Generated by Django 2.1.4 on 2019-01-14 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20190114_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='p1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p1', to='app.Users', to_field='name'),
        ),
        migrations.AlterField(
            model_name='game',
            name='p2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p2', to='app.Users', to_field='name'),
        ),
    ]
