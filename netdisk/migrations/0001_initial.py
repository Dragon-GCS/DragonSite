# Generated by Django 3.1.5 on 2021-05-31 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('digest', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('links', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='文件夹名称')),
                ('path', models.CharField(max_length=2048, unique=True, verbose_name='文件夹路径')),
                ('creat_time', models.DateField(auto_now_add=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='netdisk.folder', to_field='path')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='文件名')),
                ('digest', models.CharField(max_length=32)),
                ('size', models.IntegerField(default=0)),
                ('upload_time', models.DateField(auto_now_add=True)),
                ('path', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netdisk.folder')),
            ],
        ),
    ]