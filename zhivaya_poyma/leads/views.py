from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LeadForm

def join(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо! Ваша заявка отправлена.")
            return redirect("join")
    else:
        form = LeadForm()

    return render(request, "leads/join.html", {"form": form})