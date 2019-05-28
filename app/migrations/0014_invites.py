# Generated by Django 2.1.4 on 2019-01-14 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20190112_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField()),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='app.Users', to_field='name')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='app.Users', to_field='name')),
            ],
        ),
    ]