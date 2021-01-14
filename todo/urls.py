from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("signup/", views.register_page, name="register_page"),
    path("login/", views.user_login, name="user_login"),
    path("dashboard/", views.dashboard_page, name="dashboard_page"),
    path("create/", views.create_todo, name="create_todo"),
    path("important/", views.important_page, name="important_page"),
    path("complete/", views.completed_page, name="completed_page"),
    path("dashboard/<int:todo_pk>", views.todo_details, name="todo_details"),
    path("dashboard/<int:todo_pk>/completed", views.todo_completed, name="todo_completed"),
    path("dashboard/<int:todo_pk>/delete", views.todo_deleted, name="todo_deleted"),
]
