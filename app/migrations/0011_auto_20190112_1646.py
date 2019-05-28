# Generated by Django 2.1.4 on 2019-01-12 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_users_cur_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='last_p1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lp1', to='app.Users', to_field='name'),
        ),
        migrations.AlterField(
            model_name='records',
            name='last_p2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lp2', to='app.Users', to_field='name'),
        ),
        migrations.AlterField(
            model_name='records',
            name='last_p3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lp3', to='app.Users', to_field='name'),
        ),
    ]