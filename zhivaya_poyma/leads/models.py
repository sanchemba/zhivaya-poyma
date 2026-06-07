from django.db import models

class Lead(models.Model):
    INTEREST_CHOICES = [
        ("volunteer", "Хочу волонтёрить"),
        ("partner", "Хочу стать партнёром"),
        ("media", "Хочу написать / рассказать"),
        ("other", "Другое"),
    ]

    name = models.CharField("Имя", max_length=120)
    email = models.EmailField("Email", blank=True)
    telegram = models.CharField("Telegram", max_length=120, blank=True)
    interest_type = models.CharField("Тип обращения", max_length=20, choices=INTEREST_CHOICES)
    message = models.TextField("Сообщение", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} — {self.get_interest_type_display()}"