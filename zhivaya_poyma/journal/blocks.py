from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock


class SectionHeadingBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, label="Надзаголовок")
    title = blocks.CharBlock(required=True, label="Заголовок")
    text = blocks.TextBlock(required=False, label="Короткий текст")

    class Meta:
        template = "blocks/section_heading.html"
        icon = "title"
        label = "Заголовок секции"


class ImageWithCaptionBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, label="Изображение")
    caption = blocks.CharBlock(required=False, label="Подпись")
    credit = blocks.CharBlock(required=False, label="Автор / источник")

    class Meta:
        template = "blocks/image_with_caption.html"
        icon = "image"
        label = "Фото с подписью"


class ObservationBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label="Заголовок")
    text = blocks.TextBlock(required=True, label="Наблюдение")
    date_label = blocks.CharBlock(required=False, label="Дата / сезон")
    place = blocks.CharBlock(required=False, label="Место")

    class Meta:
        template = "blocks/observation.html"
        icon = "doc-full-inverse"
        label = "Полевое наблюдение"


class ProgressNoteBlock(blocks.StructBlock):
    stage = blocks.CharBlock(required=True, label="Этап")
    done = blocks.TextBlock(required=False, label="Что сделано")
    seen = blocks.TextBlock(required=False, label="Что наблюдаем")
    next_step = blocks.TextBlock(required=False, label="Что дальше")

    class Meta:
        template = "blocks/progress_note.html"
        icon = "tasks"
        label = "Этап восстановления"


class CTABlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, label="Текст кнопки")
    url = blocks.URLBlock(required=False, label="Внешняя ссылка")
    note = blocks.CharBlock(required=False, label="Подпись")

    class Meta:
        template = "blocks/cta_block.html"
        icon = "link"
        label = "Кнопка / призыв"

class ExternalVideoBlock(blocks.StructBlock):
    video = EmbedBlock(
        required=True,
        max_width=1200,
        max_height=800,
        label="Ссылка на видео",
        help_text="Вставьте ссылку на YouTube, VK Видео, RuTube или другой поддерживаемый сервис.",
    )
    caption = blocks.CharBlock(
        required=False,
        max_length=500,
        label="Подпись",
    )
    credit = blocks.CharBlock(
        required=False,
        max_length=300,
        label="Автор / источник",
    )

    class Meta:
        template = "blocks/external_video.html"
        icon = "media"
        label = "Видео со внешней платформы"

class LocalVideoBlock(blocks.StructBlock):
    video = DocumentChooserBlock(
        required=True,
        label="Видео файл",
        help_text="Загрузите MP4 или WebM в раздел Documents Wagtail.",
    )
    poster = ImageChooserBlock(
        required=False,
        label="Постер",
        help_text="Статичная картинка до запуска видео. Рекомендуется для длинных роликов.",
    )
    caption = blocks.CharBlock(
        required=False,
        max_length=500,
        label="Подпись",
    )
    credit = blocks.CharBlock(
        required=False,
        max_length=300,
        label="Автор / источник",
    )
    autoplay = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Запускать автоматически без звука",
    )
    loop = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Повторять видео",
    )

    class Meta:
        template = "blocks/local_video.html"
        icon = "media"
        label = "Видео файл"

