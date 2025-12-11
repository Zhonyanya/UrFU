from django.shortcuts import render


# Create your views here.
def about(request):
    """Рендер странички about"""
    return render(request, "pages/about.html")


def rules(request):
    """Рендер странички правил"""
    return render(request, "pages/rules.html")
