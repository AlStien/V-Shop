# Generated by Django 3.2.9 on 2021-11-10 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_product', '0004_rename_comments_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='picture',
            field=models.ImageField(default='products/<django.db.models.fields.UUIDField>.png', upload_to='products'),
        ),
    ]
