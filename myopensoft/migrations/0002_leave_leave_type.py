# Generated by Django 5.1.7 on 2025-03-21 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myopensoft', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='leave_type',
            field=models.CharField(choices=[('sick', 'Sick Leave'), ('casual', 'Casual Leave'), ('unpaid', 'Unpaid Leave'), ('annual', 'Annual Leave')], default=10, max_length=20),
        ),
    ]
