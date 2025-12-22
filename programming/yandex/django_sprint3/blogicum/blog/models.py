from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    """Абстрактная модель"""

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию",
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Добавлено")

    class Meta:
        abstract = True


class Category(BaseModel):
    """Категория поста"""

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        verbose_name="Идентификатор",
        help_text="Идентификатор страницы для URL; разрешены символы латиницы"
        + ", цифры, дефис и подчёркивание.",
        unique=True
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
        verbose_name="Опубликовано")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Location(BaseModel):
    """Привязка к локации"""

    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Post(BaseModel):
    """Пост с названием, текстом и датой появления"""

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text="Если установить дату и время в будущем — "
        + "можно делать отложенные публикации.",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор публикации"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        related_name="posts"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name="Категория",
        related_name="posts"
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
