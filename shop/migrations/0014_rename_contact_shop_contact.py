# Generated by Django 4.2.3 on 2023-08-13 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_orderupdate_timestamp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contact',
            new_name='Shop_Contact',
        ),
    ]