# Generated manually for profile picture support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_is_rated_customuser_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='profile_pictures/',
                verbose_name='الصورة الشخصية',
            ),
        ),
    ]
