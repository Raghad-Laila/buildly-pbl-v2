from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customuser_profile_picture'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_archived',
            field=models.BooleanField(
                default=False,
                help_text='هل تم أرشفة هذا المسار؟',
                verbose_name='مؤرشف',
            ),
        ),
        migrations.CreateModel(
            name='CourseArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الأرشفة')),
                ('course_data', models.JSONField(verbose_name='بيانات المسار المحفوظة')),
                ('archived_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='archived_courses', to='account.customuser', verbose_name='أرشفه بواسطة')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archive_records', to='courses.course', verbose_name='المسار')),
            ],
            options={
                'verbose_name': 'أرشيف مسار',
                'verbose_name_plural': 'أرشيف المسارات',
                'ordering': ['-archived_at'],
            },
        ),
    ]
