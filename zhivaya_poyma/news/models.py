from django.db import models
from django.urls import reverse

class NewsPost(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    excerpt = models.TextField("Краткое описание", blank=True)
    body = models.TextField("Текст")
    cover_image = models.ImageField("Обложка", upload_to="news/", blank=True, null=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    published_at = models.DateTimeField("Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})