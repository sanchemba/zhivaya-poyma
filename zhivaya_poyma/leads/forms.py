from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "telegram", "interest_type", "message"]
        labels = {
            "name": "Как вас зовут",
            "email": "Email",
            "telegram": "Telegram",
            "interest_type": "Чем вы хотите помочь",
            "message": "Комментарий",
        }
        help_texts = {
            "name": "Можно указать имя и фамилию или только имя.",
            "email": "Если вам удобно связываться по почте.",
            "telegram": "Если вам удобнее быстрый контакт.",
            "interest_type": "Выберите вариант, который ближе всего к вашему запросу.",
            "message": "Можно коротко написать, чем именно вы хотите быть полезны проекту.",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Например: Анна Смирнова",
                    "autocomplete": "name",
                    "maxlength": 120,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "name@example.org",
                    "autocomplete": "email",
                    "maxlength": 254,
                }
            ),
            "telegram": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "@username",
                    "autocomplete": "off",
                    "maxlength": 120,
                }
            ),
            "interest_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 6,
                    "placeholder": "Расскажите немного о себе, вашем интересе к проекту или возможном формате помощи.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].error_messages["required"] = "Пожалуйста, укажите ваше имя."
        self.fields["email"].error_messages["invalid"] = "Введите корректный email."

    def clean(self):
        cleaned_data = super().clean()
        email = (cleaned_data.get("email") or "").strip()
        telegram = (cleaned_data.get("telegram") or "").strip()

        if not email and not telegram:
            raise forms.ValidationError(
                "Пожалуйста, оставьте хотя бы один способ связи: email или Telegram."
            )

        cleaned_data["email"] = email
        cleaned_data["telegram"] = telegram
        return cleaned_data