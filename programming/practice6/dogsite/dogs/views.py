from django.shortcuts import render
import requests

# Create your views here.
def get_dogs(request):
    """
    Выдаёт картинки с собаками по заданным в поле ввода собакам

    Args:
        request: Реквест
    """
    response = requests.get("https://dog.ceo/api/breeds/list/all")
    breedslist = list(response.json()["message"].keys())
    entered_breeds = request.GET.get("input_field")
    imagelist = []
    if entered_breeds != None:
        entered_breeds = entered_breeds.replace(",", " ").split()
        for breed in entered_breeds:
            image_url = f"https://dog.ceo/api/breed/{breed}/images/random"
            image_response = requests.get(image_url).json()["message"]
            imagelist.append(image_response)

    return render(request, "dogs/dogs_viewer.html",
                   {"breedslist": breedslist, "imagelist": imagelist})