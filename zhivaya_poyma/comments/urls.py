from django.urls import path

from .views import post_comment

app_name = "comments"

urlpatterns = [
    path("post/<int:page_id>/", post_comment, name="post"),
]