"""Migrations to switch from sorl ImageField to a new package field."""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('newsletter', '0005_auto_20190918_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='newsletter/images/%Y/%m/%d',
                verbose_name='image'
            ),
        ),
    ]
