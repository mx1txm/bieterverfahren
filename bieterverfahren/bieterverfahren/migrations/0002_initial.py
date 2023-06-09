# Generated by Django 4.1.5 on 2023-03-12 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bieterverfahren", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Seller",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("photo", models.ImageField(upload_to="property_photos")),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to="bieterverfahren.seller",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BiddingProcess",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "starting_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "minimum_increment",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "duration_extension_time",
                    models.DurationField(
                        default="0h:10m", help_text="Duration extends 10 minutes"
                    ),
                ),
                (
                    "property",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bidding_process",
                        to="bieterverfahren.property",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bid",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bidder_name", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "bidding_process",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bids",
                        to="bieterverfahren.biddingprocess",
                    ),
                ),
            ],
            options={
                "ordering": ["-amount", "created_at"],
            },
        ),
    ]
