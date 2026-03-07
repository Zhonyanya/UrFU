from django.db import models

# Create your models here.
class Email(models.Model):
    """Модель письма"""
    subject = models.CharField(
        max_length=100,
        verbose_name="Тема"
    )
    content = models.TextField(
        verbose_name="Содержимое"
    )
    sender = models.TextField(
        verbose_name="Отправитель"
    )
    recipient = models.TextField(
        verbose_name="Получатель"
    )
    sent_by_you = models.BooleanField(
        verbose_name="Отправлено вами",
        default=False
    )
    trashed = models.BooleanField(
        verbose_name="В корзине",
        default=False
    )
    archived = models.BooleanField(
        verbose_name="В архиве",
        default=False
    )