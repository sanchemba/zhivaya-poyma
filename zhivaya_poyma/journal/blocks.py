from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


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