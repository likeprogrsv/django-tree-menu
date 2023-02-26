# Generated by Django 4.1.7 on 2023-02-24 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_category_menu_name_alter_category_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='is_active',
        ),
        migrations.AddField(
            model_name='category',
            name='position_on_curr_category',
            field=models.IntegerField(default=0),
        ),
    ]
