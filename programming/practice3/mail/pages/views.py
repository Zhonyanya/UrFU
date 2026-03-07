from django.shortcuts import render, get_object_or_404
from .models import Email

# Create your views here.
def index(request):
    """Отображает главную страницу"""
    inbox_emails = Email.objects.all()
    context = {
        "inbox_emails": inbox_emails
    }
    return render(request, "pages/index.html", context)

def sent_messages(request):
    """Отображает страницу отправленных сообщений"""
    emails = Email.objects.all()
    context = {
        "emails": emails
    }
    return render(request, "pages/sent.html", context)

def email_detail(request, email_id):
    """Отображает детали сообщения"""
    letter = get_object_or_404(
        Email, pk=email_id
    )
    return render(request, 'pages/letter_info.html', {"letter": letter})

def trash_bin(request):
    """Отображает мусорку"""
    emails = Email.objects.all()
    context = {
        "emails": emails
    }
    return render(request, "pages/trashbin.html", context)

def archive(request):
    """Отображает архив"""
    emails = Email.objects.all()
    context = {
        "emails": emails
    }
    return render(request, "pages/archived.html", context)