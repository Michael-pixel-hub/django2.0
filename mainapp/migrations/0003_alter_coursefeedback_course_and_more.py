# Generated by Django 4.1.1 on 2022-10-06 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_lesson_options_alter_news_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursefeedback',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.courses', verbose_name='Courses'),
        ),
        migrations.AlterField(
            model_name='coursefeedback',
            name='rating',
            field=models.SmallIntegerField(choices=[(1, '*'), (2, '**'), (3, '***'), (4, '****'), (5, '*****')], default=5, verbose_name='Rating'),
        ),
    ]
