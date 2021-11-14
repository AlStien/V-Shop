# Generated by Django 3.2.9 on 2021-11-14 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.CharField(choices=[(1, 'poor'), (2, 'unsatisfactory'), (3, 'average'), (4, 'good'), (5, 'excellent')], default=1, max_length=1),
        ),
    ]
