# Generated by Django 4.1 on 2022-08-27 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0004_alter_orderitem_order"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="Customer",
            new_name="customer",
        ),
        migrations.AlterField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="customer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orderitem",
                to="store.order",
            ),
        ),
    ]
