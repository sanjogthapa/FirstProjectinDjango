# Generated by Django 3.1.1 on 2020-09-30 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_mgmt_sys', '0002_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='cover_photo',
            field=models.ImageField(default='fed 1.jpg', upload_to='books_photos'),
        ),
    ]
