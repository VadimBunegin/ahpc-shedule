# Generated by Django 4.0.2 on 2022-05-07 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_rename_ratefact_productratefact_reviewratefact'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='auditory',
            field=models.CharField(default='1', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='auditory_friday',
            field=models.CharField(default='1', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='auditory_saturday',
            field=models.CharField(default='1', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='auditory_thursday',
            field=models.CharField(default='1', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='auditory_tuesday',
            field=models.CharField(default='1', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='auditory_wednesday',
            field=models.CharField(default='1', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='comments',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='comments_friday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='comments_saturday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='comments_thursday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='comments_tuesday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='comments_wednesday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='friday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='monday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='saturday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='teacher',
            field=models.CharField(default='-', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='teacher_friday',
            field=models.CharField(default='-', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='teacher_saturday',
            field=models.CharField(default='-', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='teacher_thursday',
            field=models.CharField(default='-', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='teacher_tuesday',
            field=models.CharField(default='-', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='teacher_wednesday',
            field=models.CharField(default='-', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='thursday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='time',
            field=models.CharField(default='00:00', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='tuesday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='Лекция', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='type_friday',
            field=models.CharField(default='Лекция', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='type_saturday',
            field=models.CharField(default='Лекция', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='type_thursday',
            field=models.CharField(default='Лекция', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='type_tuesday',
            field=models.CharField(default='Лекция', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='type_wednesday',
            field=models.CharField(default='Лекция', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='wednesday',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='week',
            field=models.IntegerField(default=1),
        ),
    ]
