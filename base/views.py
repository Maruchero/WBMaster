from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required

from base.models import *

# Create your views here.


def index(request):
    return render(request, "index.html")


def docs(request):
    return render(request, "docs.html")


def logout(request):
    user_logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("/")


def login(request):
    # Context
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Field checks

        # Login user
        if not errors:
            user = authenticate(username=email, password=password)
            if user:
                # User is authenticated
                user_login(request, user)
                # Add role
                role = Role.objects.filter(user_id=user.id).first()
                user.role = role
                return redirect("/dashboard/", {"user": user, "role": role})
            else:
                context["form"] = {
                    "email": email,
                    "password": password,
                }
                messages.error(request, "Invalid credentials")
                errors["credentials"] = "Invalid credentials"
                return render(request, "login.html", context)

    return render(request, "login.html")


def register(request):
    # Context
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        role = request.POST["role"]

        # Field checks
        if User.objects.filter(username=email).exists():
            errors["email"] = "Email already in use"
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match"

        # Register user
        if not errors:
            try:
                user = User.objects.create_user(
                    username=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                user_role = Role.objects.create(role=role, user=user)
                user_role.save()

                messages.success(request, "Account succesfully created")

                return redirect("/login/")
            except:
                messages.error(request, "Registration failed")
        else:
            context["form"] = {
                "email": email,
                "password": password,
                "confirm_password": confirm_password,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
            }

    return render(request, "register.html", context)


@login_required(login_url='/login/')
def dashboard(request):
    context = {}

    # Role
    role = Role.objects.filter(user_id=request.user.id).first()
    if not role:
        redirect("/logout/")
    context["role"] = role.role

    # Projects
    projects = Project.objects.filter(created_by_id=request.user.id)
    context["projects"] = projects

    # Render
    return render(request, "dashboard.html", context=context)


@login_required(login_url='/login/')
def add_project(request):
    context = {}
    errors = {}
    context["errors"] = errors
    
    # Role
    role = Role.objects.filter(user_id=request.user.id).first()
    if not role:
        redirect("/logout/")
    if role != "project_manager":
        redirect("/dashboard/")

    # If the form has been submitted
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        picture = request.FILES["picture"]

        # Add project
        project = Project.objects.create(
            name=name,
            description=description,
            picture=picture,
            created_by=request.user
        )
        project.save()

    return render(request, "add_project.html")
