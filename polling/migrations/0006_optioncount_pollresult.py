# Generated by Django 3.1.1 on 2020-10-02 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0005_auto_20201003_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling.option')),
            ],
        ),
        migrations.CreateModel(
            name='PollResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_count', models.ManyToManyField(to='polling.OptionCount')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='polling.poll')),
            ],
        ),
    ]
