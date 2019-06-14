# Generated by Django 2.1.5 on 2019-05-30 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('lastlogin', models.CharField(blank=True, max_length=255, null=True)),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('star', models.CharField(blank=True, max_length=255, null=True)),
                ('viewcount', models.IntegerField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('like', models.IntegerField(blank=True, null=True)),
                ('addtime', models.DateTimeField(auto_now=True, null=True)),
                ('tag', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.IntegerField(blank=True, null=True)),
                ('public', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'blog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('addtime', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('site', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('addtime', models.DateTimeField(auto_now=True, null=True)),
                ('repaly', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('addtime', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'rss',
                'managed': False,
            },
        ),
    ]
