# Generated by Django 4.2.2 on 2024-05-10 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='link',
            new_name='url',
        ),
    ]