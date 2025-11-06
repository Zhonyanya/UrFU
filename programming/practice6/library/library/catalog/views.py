from django.shortcuts import render

# Create your views here.
def book_list(request):
    books = [
        {
            "title": "Невероятная книга",
            "author": "Крутой парень",
            "year": "1337"
        },
        {
            "title": "Книжная братва",
            "author": "Нормальный парень",
            "year": "1338",
        }
    ]
    return render(request, "catalog/view_books.html", {"books": books})
