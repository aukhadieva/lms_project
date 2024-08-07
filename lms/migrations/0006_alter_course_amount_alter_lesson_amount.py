# Generated by Django 4.2.13 on 2024-07-04 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_course_amount_lesson_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='стоимость курса'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='стоимость урока'),
        ),
    ]
