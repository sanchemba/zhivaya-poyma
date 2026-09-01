from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page

from .blocks import (
    CTABlock,
    ImageWithCaptionBlock,
    ObservationBlock,
    ProgressNoteBlock,
    SectionHeadingBlock,
    ExternalVideoBlock,
    LocalVideoBlock
)

from pathlib import Path

class JournalIndexPage(Page):
    intro = models.TextField(blank=True, verbose_name="Вводный текст")

    max_count = 1
    subpage_types = ["journal.JournalPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    template = "journal/journal_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["entries"] = (
            JournalPage.objects
            .child_of(self)
            .live()
            .public()
            .order_by("-first_published_at")
        )
        return context


class JournalPage(Page):

    @property
    def cover_is_animated_gif(self):
        if not self.cover_image:
            return False
        return Path(self.cover_image.file.name).suffix.lower() == ".gif"

    subtitle = models.CharField(
        max_length=1000,
        blank=True,
        verbose_name="Краткое описание",
    )

    event_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата записи",
        help_text=(
            "Дата события или наблюдения. "
            "Если не заполнена, будет показана дата публикации."
        ),
    )

    cover_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Обложка",
    )

    cover_caption = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Подпись к обложке",
    )

    cover_credit = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Автор / источник обложки",
    )

    body = StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(
                    features=[
                        "h3",
                        "h4",
                        "bold",
                        "italic",
                        "link",
                        "ol",
                        "ul",
                        "blockquote",
                    ],
                    label="Текст",
                ),
            ),
            ("heading_section", SectionHeadingBlock()),
            ("image_with_caption", ImageWithCaptionBlock()),
            ("observation", ObservationBlock()),
            ("progress_note", ProgressNoteBlock()),
            ("cta", CTABlock()),
            ("external_video", ExternalVideoBlock()),
            ("local_video", LocalVideoBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Содержимое записи",
    )

    parent_page_types = ["journal.JournalIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("event_date"),
        FieldPanel("cover_image"),
        FieldPanel("cover_caption"),
        FieldPanel("cover_credit"),
        FieldPanel("body"),
    ]

    template = "journal/journal_page.html"