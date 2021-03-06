# Generated by Django 3.1.1 on 2020-10-02 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20200922_0950'),
        ('polling', '0006_optioncount_pollresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling.optioncount')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling.pollresult')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.userinfo')),
            ],
        ),
        migrations.AddField(
            model_name='pollresult',
            name='voted_users',
            field=models.ManyToManyField(to='polling.UserPoll'),
        ),
    ]
