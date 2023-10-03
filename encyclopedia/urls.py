from django.urls import path
from encyclopedia.views import *

urlpatterns = [
    path("", index, name="index"),
    path("wiki/<str:title>", wiki, name="entry"),
    path("random/", random_entry, name='random_entry'),
    path("edit/<str:title>", edit_entry, name='edit_entry'),
    path("save/<str:title>", save_entry, name='save_entry')
]
