# Generated by Django 4.2.6 on 2023-10-23 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemauth', '0002_alter_user_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='secret_key',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
