# Generated by Django 4.2.7 on 2023-11-09 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_newsarticle_article_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="articlecomment",
            name="likes",
            field=models.IntegerField(default=0),
        ),
    ]
