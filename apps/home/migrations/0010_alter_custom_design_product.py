# Generated by Django 3.2.6 on 2022-05-08 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_plainproduct_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_design',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.plainproduct'),
        ),
    ]