from django.urls import path
from . import views

urlpatterns = [
    path('id/<int:email_id>/', views.email_detail, name="email_detail"),
    path('sent/', views.sent_messages, name="sent"),
    path('trash/', views.trash_bin, name="trash"),
    path('archive/', views.archive, name="archive")
]