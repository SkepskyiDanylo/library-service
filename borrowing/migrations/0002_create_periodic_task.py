from django.db import migrations
import json


def create_check_borrowings_task(apps, schema_editor):
    CrontabSchedule = apps.get_model("django_celery_beat", "CrontabSchedule")
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")

    schedule, created = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="8",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
    )

    PeriodicTask.objects.update_or_create(
        name="Check overdue borrowings",
        defaults={
            "crontab": schedule,
            "task": "borrowings.tasks.check_borrowings",
            "args": json.dumps([]),
        },
    )


def delete_check_borrowings_task(apps, schema_editor):
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    PeriodicTask.objects.filter(name="Check overdue borrowings").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("borrowing", "0001_initial"),
        ("django_celery_beat", "0019_alter_periodictasks_options"),
    ]

    operations = [
        migrations.RunPython(
            create_check_borrowings_task, delete_check_borrowings_task
        ),
    ]
