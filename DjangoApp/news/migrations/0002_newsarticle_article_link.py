# Generated by Django 4.2.7 on 2023-11-06 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsarticle",
            name="article_link",
            field=models.URLField(default=""),
        ),
    ]