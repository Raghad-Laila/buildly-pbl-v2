from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customuser_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('course', 'مسار'), ('project', 'مشروع')], max_length=10, verbose_name='نوع العنصر')),
                ('object_id', models.PositiveIntegerField(verbose_name='معرف العنصر')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='account.customuser', verbose_name='المستخدم')),
            ],
            options={
                'verbose_name': 'مفضلة',
                'verbose_name_plural': 'المفضلة',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='userfavorite',
            constraint=models.UniqueConstraint(fields=('user', 'item_type', 'object_id'), name='unique_user_favorite_item'),
        ),
    ]
