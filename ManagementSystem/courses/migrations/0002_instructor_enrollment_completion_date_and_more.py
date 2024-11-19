# Generated by Django 5.0.3 on 2024-11-15 21:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='enrollment',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to=settings.AUTH_USER_MODEL),
        ),
    ]