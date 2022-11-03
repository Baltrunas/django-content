# Generated by Django 3.2.12 on 2022-04-19 14:38

from django.db import migrations, models
import django.db.models.deletion
import helpful.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Vorname')),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='Title')),
                ('header', models.CharField(blank=True, max_length=256, null=True, verbose_name='Header')),
                ('keywords', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Keywords')),
                ('description', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Beschreibung')),
                ('head_code', models.TextField(blank=True, null=True, verbose_name='Head code')),
                ('footer_code', models.TextField(blank=True, null=True, verbose_name='Footer code')),
                ('img', models.FileField(blank=True, upload_to=helpful.fields.upload_to, verbose_name='Bild')),
                ('intro', models.TextField(blank=True, null=True, verbose_name='Intro')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('slug', models.CharField(max_length=128, unique=True, verbose_name='Webserverebene')),
                ('url', models.CharField(editable=False, max_length=1024, verbose_name='URL')),
                ('position', models.PositiveIntegerField(default=500, verbose_name='Position')),
                ('template', models.CharField(blank=True, max_length=32, null=True, verbose_name='Template')),
                ('public', models.BooleanField(default=True, verbose_name='Gesetzlich Versicherte')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='content.page', verbose_name='parent')),
                ('sites', models.ManyToManyField(blank=True, related_name='pages', to='sites.Site', verbose_name='Websites')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['position'],
                'base_manager_name': 'objects',
            },
        ),
    ]