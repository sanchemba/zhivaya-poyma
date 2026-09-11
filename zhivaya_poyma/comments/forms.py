from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["author_name", "author_email", "text"]
        widgets = {
            "author_name": forms.TextInput(
                attrs={
                    "placeholder": "Как к вам обращаться",
                    "autocomplete": "name",
                    "maxlength": 80,
                }
            ),
            "author_email": forms.EmailInput(
                attrs={
                    "placeholder": "E-mail — необязательно",
                    "autocomplete": "email",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Оставьте бережный комментарий или вопрос",
                    "rows": 5,
                    "maxlength": 2000,
                }
            ),
        }

    def clean_website(self):
        if self.cleaned_data["website"]:
            raise forms.ValidationError("Не удалось отправить комментарий.")
        return ""