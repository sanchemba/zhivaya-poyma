from django.core.validators import MinLengthValidator
from django.db import models

from journal.models import JournalPage


class Comment(models.Model):
    page = models.ForeignKey(
        JournalPage,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Запись дневника",
    )

    author_name = models.CharField(
        "Имя",
        max_length=80,
    )

    author_email = models.EmailField(
        "E-mail",
        blank=True,
        help_text="Не публикуется. Нужен только для обратной связи.",
    )

    text = models.TextField(
        "Комментарий",
        max_length=2000,
        validators=[MinLengthValidator(3)],
    )

    is_approved = models.BooleanField(
        "Одобрен",
        default=False,
    )

    created_at = models.DateTimeField(
        "Отправлен",
        auto_now_add=True,
    )

    moderated_at = models.DateTimeField(
        "Промодерирован",
        blank=True,
        null=True,
    )

    ip_address = models.GenericIPAddressField(
        "IP-адрес",
        blank=True,
        null=True,
    )

    user_agent = models.CharField(
        "User-Agent",
        max_length=500,
        blank=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author_name}: {self.text[:60]}"