import os
from django.core.files import File
from wagtail.images.models import Image
from news.models import NewsPost
from journal.models import JournalIndexPage, JournalPage

index = JournalIndexPage.objects.get(slug="project-journal")

for old in NewsPost.objects.filter(is_published=True).order_by("published_at"):
    if JournalPage.objects.child_of(index).filter(slug=old.slug).exists():
        print(f"SKIP: {old.slug}")
        continue

    # 1. Сначала обрабатываем и переносим изображение
    wagtail_image = None
    if old.cover_image:
        try:
            # Получаем имя файла из старого ImageFieldFile
            file_name = os.path.basename(old.cover_image.name)
            
            # Открываем существующий файл в Django File
            django_file = File(old.cover_image.file, name=file_name)
            
            # Создаем объект Image для Wagtail
            wagtail_image = Image.objects.create(
                title=f"Cover for {old.title[:40]}", # Ограничиваем длину заголовка картинки
                file=django_file
            )
        except Exception as e:
            print(f"ERROR temporary reading image for {old.slug}: {e}")
            # Если картинка повреждена или удалена с диска, скрипт не упадет, а продолжит без нее
            wagtail_image = None

    # 2. Создаем страницу с правильным объектом в cover_image
    page = JournalPage(
        title=old.title,
        slug=old.slug,
        subtitle=old.excerpt or "",
        event_date=old.published_at.date() if old.published_at else None,
        cover_image=wagtail_image, # Передаем объект Wagtail Image вместо ImageFieldFile
        body=[
            ("paragraph", old.body or ""),
        ],
    )

    # 3. Сохраняем и публикуем страницу в Wagtail
    index.add_child(instance=page)
    page.save_revision().publish()

    print(f"OK: {page.slug}")

