from django.shortcuts import render
from news.models import NewsPost
from journal.models import JournalPage

def home(request):

    latest_news = NewsPost.objects.filter(is_published=True).order_by("-published_at")[:3]

    latest_journal = (
        JournalPage.objects
        .live()
        .public()
        .order_by("-first_published_at")[:3]
    )

    return render(
        request,
        "core/home.html",
        {
            "latest_news": latest_news,
            "latest_journal": latest_journal,
        },
    )

    #return render(request, "core/home.html", {"latest_news": latest_news})

def about(request):
    return render(request, "core/about.html")

def contacts(request):
    return render(request, "core/contacts.html")