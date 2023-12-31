# Generated by Django 4.2.4 on 2023-09-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_comment_description_en_comment_description_fa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bio_en',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='بایوگرافی'),
        ),
        migrations.AddField(
            model_name='account',
            name='bio_fa',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='بایوگرافی'),
        ),
        migrations.AddField(
            model_name='account',
            name='job_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='شغل'),
        ),
        migrations.AddField(
            model_name='account',
            name='job_fa',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='شغل'),
        ),
    ]
