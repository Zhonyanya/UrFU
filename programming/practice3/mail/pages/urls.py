from django.urls import path
from . import views

urlpatterns = [
    path('id/<int:email_id>/', views.email_detail, name="email_detail"),
    path('folders/', views.list_folders, name="list_folders"),
    path('folder/<str:folder_name>/', views.folder_view, name="folder_view"),
    path('send/', views.compose_email, name="send"),
    path('move/<int:email_id>/<str:target_folder>/', views.move_to_folder,
          name='move_to_folder')
]