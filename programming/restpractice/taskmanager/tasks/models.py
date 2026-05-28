from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
    """Модель проекта."""

    name = models.CharField(verbose_name="Название", max_length=128)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_projects',
        verbose_name='Создатель'
    )
    members = models.ManyToManyField(
        User,
        related_name='projects',
        verbose_name='Участники'
    )


class Task(models.Model):
    """Модель задачи."""

    priorities = [
        ('LOW', 'Низкий'),
        ("MEDUIM", "Средний"),
        ("HIGH", "Высокий")
    ]

    statuses = [
        ("TODO", "Нужно сделать"),
        ("IN PROGRESS", "В процессе"),
        ("DONE", "Сделано")
    ]

    title = models.CharField(verbose_name="Заголовок", max_length=128)
    description = models.CharField(verbose_name="Описание")
    priority = models.CharField(
        verbose_name="Приоритет",
        choices=priorities,
        default="MEDUIM"
    )

    status = models.CharField(
        verbose_name="Статус",
        choices=statuses,
        default="TODO"
    )
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Проект"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_tasks",
        verbose_name="Автор"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        verbose_name="Исполнитель"
    )
