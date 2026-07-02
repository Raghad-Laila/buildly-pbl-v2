from django.db import migrations


def backfill_project_languages(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.all():
        if not project.languages and project.language:
            project.languages = [project.language]
            project.save(update_fields=['languages'])


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_project_languages_multiselect'),
    ]

    operations = [
        migrations.RunPython(backfill_project_languages, migrations.RunPython.noop),
    ]
