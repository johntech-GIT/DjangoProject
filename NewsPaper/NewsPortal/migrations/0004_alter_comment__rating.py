# Generated by Django 4.2.1 on 2023-05-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPortal', '0003_rename_rating_post__rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='_rating',
            field=models.IntegerField(db_column='rating', default=0),
        ),
    ]
