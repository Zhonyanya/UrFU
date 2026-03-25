from django.db import models

class Folder(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название папки"
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Описание"
    )
    def get_emails(self):
        """Получить все письма в папке"""
        return self.emails.all()

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
    is_read = models.BooleanField(
        default=False,
        verbose_name="Прочитано"
    )

    folders = models.ManyToManyField(
        Folder,
        related_name="emails",
        blank=True,
        verbose_name="Папки"
    )

    def mark_as_read(self):
        """Отметить как прочитанное"""
        self.is_read = True
        self.save()

    def move_to_folder(self, folder_name):
        """Переместить в папку"""
        folder = Folder.objects.get(name=folder_name)
        self.folders.clear()
        self.folders.add(folder)
        return folder

    def archive(self):
        """Архивировать"""
        return self.move_to_folder("Архив")

    def trash(self):
        """Отправить в мусорку"""
        return self.move_to_folder("Корзина")

    def delete(self):
        """Удалить"""
        return self.move_to_folder("Удалённое")

    def to_inbox(self):
        """Закинуть во входящие"""
        return self.move_to_folder("Входящие")

    def sent(self):
        """Закинуть в исходящие"""
        return self.move_to_folder("Исходящие")
