from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks

from .blocks import (
    SectionHeadingBlock,
    ImageWithCaptionBlock,
    ObservationBlock,
    ProgressNoteBlock,
    CTABlock,
)


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
            JournalPage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
        )
        return context


class JournalPage(Page):
    subtitle = models.CharField(max_length=220, blank=True, verbose_name="Подзаголовок")
    lead = models.TextField(blank=True, verbose_name="Лид")

    body = StreamField(
        [
            ("heading_section", SectionHeadingBlock()),
            ("paragraph", blocks.RichTextBlock(features=[
                "h3", "h4", "bold", "italic", "link", "ol", "ul", "blockquote"
            ])),
            ("image_with_caption", ImageWithCaptionBlock()),
            ("observation", ObservationBlock()),
            ("progress_note", ProgressNoteBlock()),
            ("cta", CTABlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Содержимое записи",
    )

    parent_page_types = ["journal.JournalIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("lead"),
        FieldPanel("body"),
    ]

    template = "journal/journal_page.html"