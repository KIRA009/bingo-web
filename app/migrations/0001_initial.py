# Generated by Django 2.1.4 on 2018-12-23 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField(unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('password', models.TextField()),
                ('validated', models.BooleanField(default=False)),
                ('secret', models.TextField(default='')),
                ('reset', models.TextField(default='')),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='p1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p1', to='app.Users', to_field='name'),
        ),
        migrations.AddField(
            model_name='game',
            name='p2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p2', to='app.Users', to_field='name'),
        ),
    ]