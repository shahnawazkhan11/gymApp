# Generated by Django 5.1.3 on 2025-01-11 22:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('weight_unit', models.CharField(default='kg', max_length=2)),
                ('neck', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('shoulders', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('left_bicep', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('right_bicep', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('left_tricep', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('right_tricep', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('left_forearm', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('right_forearm', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('upper_abs', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('waist', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('hips', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('left_calf', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('right_calf', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('left_thigh', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('right_thigh', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
