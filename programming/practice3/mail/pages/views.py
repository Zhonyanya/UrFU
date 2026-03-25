from django.shortcuts import render, get_object_or_404, redirect
from .models import Email, Folder

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
    if not letter.is_read:
        letter.mark_as_read()
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

def list_folders(request):
    """Показать все папки"""
    folders = Folder.objects.all()
    folders_data = []
    for folder in folders:
        folders_data.append({
            "name": folder.name,
            "description": folder.description
        })
    return render(request, "pages/folders.html", {"folders": folders_data})

def folder_view(request, folder_name):
    """Чекнуть письма в конкретной папке"""
    folder = Folder.objects.get(name=folder_name)
    emails = folder.get_emails()
    context = {
        "emails": emails,
        "folder_name": folder_name,
        "folders": Folder.objects.all()
    }
    return render(request, "pages/folder_view.html", context)

def compose_email(request):
    """Составить имейл"""
    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        content = request.POST.get("content", "").strip()
        recipient = request.POST.get("recipient", "").strip()
        email = Email.objects.create(
            subject=subject,
            content=content,
            recipient=recipient,
            sender="Вы"
        )
        email.save()
        email.move_to_folder("Исходящие")
    return render(request, "pages/new_letter.html")

def move_to_folder(request, email_id, target_folder):
    """Переместить письмо в папку"""
    email = get_object_or_404(Email, id=email_id)

    email.move_to_folder(target_folder)
    return redirect(request.META.get('HTTP_REFERER', 'index'))
