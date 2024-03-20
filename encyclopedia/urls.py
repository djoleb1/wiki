from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>", views.render_wiki, name="renderwiki"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/", views.edit, name="edit"),
    path("randompage/", views.randompage, name="randompage")
]
