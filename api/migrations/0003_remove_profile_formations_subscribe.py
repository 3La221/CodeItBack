# Generated by Django 4.2.3 on 2024-04-13 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_profile_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='formations',
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.BooleanField(default=False)),
                ('formation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.formation')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
