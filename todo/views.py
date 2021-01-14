from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import NewUserTodo
from . import forms


def home_page(request):
    return render(request, 'base.html')


def register_page(request):

    if request.method == "POST":
        user = forms.NewUserForm(request.POST)

        if user.is_valid():
            user = user.save()
            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("todo:dashboard_page")

        else:
            print(user.errors)
    else:
        user = forms.NewUserForm()

    return render(request, 'todo/register.html', dict(form=user))


def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("todo:dashboard_page")

            else:
                return render(request, 'todo/login.html', {"error": "Account has been Deactivated"})
        else:
            return render(request, 'todo/login.html', {"error": "Invalid password for the given Username"})

    return render(request, 'todo/login.html', {})


@login_required
def dashboard_page(request):
    todos = NewUserTodo.objects.filter(
        user=request.user, date_completed__isnull=True)
    no_todo = None
    if not todos:
        no_todo = 'Opps! You have no todos yet, click the "Create" button to start.'
    return render(request, 'todo/dashboard.html', dict(todos=todos, no_todo=no_todo))


@login_required
def completed_page(request):
    todos = NewUserTodo.objects.filter(
        user=request.user, date_completed__isnull=False).order_by("-date_completed")
    no_todo = None
    if not todos:
        no_todo = 'Opps! You haven\'t completed any todos yet.'
    return render(request, 'todo/completed_page.html', dict(todos=todos, no_todo=no_todo))


@login_required
def important_page(request):
    todos = NewUserTodo.objects.filter(
        user=request.user, important=True, date_completed__isnull=True).order_by("-important")
    no_todo = None
    if not todos:
        no_todo = 'Opps! No important todos.'
    return render(request, 'todo/important_page.html', dict(todos=todos, no_todo=no_todo))


@login_required
def create_todo(request):
    if request.method == "POST":
        try:
            form = forms.NewUserTodoForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("todo:dashboard_page")
            else:
                return render(request, 'todo/create_todo.html', dict(form=form))

        except ValueError:
            return render(request, 'todo/create_todo.html', dict(form=form))
    else:
        form = forms.NewUserTodoForm()
    return render(request, 'todo/create_todo.html', dict(form=form))


@login_required
def todo_details(request, todo_pk=None):
    todo = get_object_or_404(NewUserTodo, pk=todo_pk, user=request.user)
    # if a user wants to update his/her form
    if request.method == "POST":
        try:
            form = forms.NewUserTodoForm(request.POST, instance=todo)
            form.save()
            return redirect("todo:dashboard_page")
        except ValueError:
            return render(request, "todo/details.html", dict(todo=todo, form=form, error="Bad Request Made!"))
    else:
        form = forms.NewUserTodoForm(instance=todo)
    return render(request, "todo/details.html", dict(todo=todo, form=form))


@login_required
def todo_completed(request, todo_pk=None):
    todo = get_object_or_404(NewUserTodo, pk=todo_pk, user=request.user)

    if request.method == "POST":
        todo.date_completed = timezone.now()
        todo.save()
        return redirect("todo:dashboard_page")


@login_required
def todo_deleted(request, todo_pk=None):
    todo = get_object_or_404(NewUserTodo, pk=todo_pk, user=request.user)

    if request.method == "POST":
        todo.delete()
        return redirect("todo:dashboard_page")


@login_required
def user_logout(request):
    logout(request)
    return redirect("todo:home_page")
