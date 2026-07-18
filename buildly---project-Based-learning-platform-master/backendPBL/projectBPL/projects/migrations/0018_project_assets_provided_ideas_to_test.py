# Generated manually to match an already-applied migration recorded in the local DB.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='assets_provided',
            field=models.JSONField(blank=True, default=list, verbose_name='الأصول المتوفرة'),
        ),
        migrations.AddField(
            model_name='project',
            name='ideas_to_test',
            field=models.JSONField(blank=True, default=list, verbose_name='أفكار للاختبار'),
        ),
    ]
