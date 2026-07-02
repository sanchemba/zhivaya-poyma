from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image, ImageOps


class NewsPost(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    excerpt = models.TextField("Краткое описание", blank=True)
    body = RichTextUploadingField(verbose_name="Текст")
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
        return reverse("news:news_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if self.cover_image:
            self.cover_image = self._compress_image(self.cover_image)
        super().save(*args, **kwargs)

    def _compress_image(self, uploaded_image):
        img = Image.open(uploaded_image)
        img = ImageOps.exif_transpose(img)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        max_size = (1600, 1600)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=82, optimize=True, progressive=True)
        buffer.seek(0)

        original_name = Path(uploaded_image.name).stem
        new_name = f"{original_name}.jpg"

        return ContentFile(buffer.read(), name=new_name)
        