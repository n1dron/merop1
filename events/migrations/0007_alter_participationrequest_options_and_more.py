# Generated by Django 5.1.4 on 2025-04-08 18:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_team_options_team_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participationrequest',
            options={'ordering': ['-created_at'], 'verbose_name': 'Заявка на участие', 'verbose_name_plural': 'Заявки на участие'},
        ),
        migrations.AlterModelOptions(
            name='qualification',
            options={'ordering': ['name'], 'verbose_name': 'Квалификация', 'verbose_name_plural': 'Квалификации'},
        ),
        migrations.AlterModelOptions(
            name='sporttype',
            options={'ordering': ['name'], 'verbose_name': 'Вид спорта', 'verbose_name_plural': 'Виды спорта'},
        ),
        migrations.AddField(
            model_name='event',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='events', to='events.team', verbose_name='Команды'),
        ),
        migrations.AddField(
            model_name='team',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_teams', to='events.event', verbose_name='Мероприятие'),
        ),
        migrations.AlterField(
            model_name='participationrequest',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participation_requests', to='events.team', verbose_name='Команда'),
        ),
        migrations.AlterField(
            model_name='participationrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participation_requests', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='teams', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
        migrations.AlterUniqueTogether(
            name='participationrequest',
            unique_together={('user', 'team')},
        ),
    ]
