# Generated by Django 2.2.2 on 2019-07-04 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_auto_20190704_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomschedule',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.Status'),
        ),
    ]
