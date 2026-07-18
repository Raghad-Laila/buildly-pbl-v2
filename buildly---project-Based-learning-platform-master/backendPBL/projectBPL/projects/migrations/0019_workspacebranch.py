# Generated manually for FR-7.3 Virtual Branches (Phase 1).

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_project_assets_provided_ideas_to_test'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkspaceBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('files_json', models.TextField(blank=True, default='')),
                ('is_main', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'project',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='workspace_branches',
                        to='projects.project',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='workspace_branches',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Workspace Branch',
                'verbose_name_plural': 'Workspace Branches',
                'ordering': ['-is_main', 'name'],
                'constraints': [
                    models.UniqueConstraint(
                        fields=('user', 'project', 'name'),
                        name='unique_branch_name_per_user_project',
                    ),
                    models.UniqueConstraint(
                        condition=models.Q(('is_main', True)),
                        fields=('user', 'project'),
                        name='unique_main_branch_per_user_project',
                    ),
                ],
            },
        ),
    ]
