from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from ratelimit.decorators import ratelimit

from journal.models import JournalPage
from .forms import CommentForm


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@require_POST
@ratelimit(key="ip", rate="5/h", method="POST", block=True)
def post_comment(request, page_id):
    page = get_object_or_404(JournalPage.objects.live(), id=page_id)

    if not page.allow_comments:
        raise Http404

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.page = page
        comment.ip_address = get_client_ip(request)
        comment.user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        comment.save()

        messages.success(
            request,
            "Спасибо. Комментарий отправлен и появится после модерации.",
        )
    else:
        messages.error(
            request,
            "Проверьте, пожалуйста, имя и текст комментария.",
        )

    return redirect(f"{page.url}#comments")