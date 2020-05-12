# Generated by Django 3.0.6 on 2020-05-07 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecurrenceDemo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetingtime',
            old_name='meeting_time',
            new_name='recurrence',
        ),
        migrations.AlterField(
            model_name='meetingtime',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_times', to='RecurrenceDemo.Course'),
        ),
    ]