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

        # Login user
        user = authenticate(username=email, password=password)
        if user:
            # User is authenticated
            user_login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("/dashboard/", context=context)
        else:
            context["form"] = {
                "email": email,
                "password": password,
            }
            messages.error(request, "Invalid credentials")
            errors["credentials"] = "Invalid credentials"
            return render(request, "login.html", context=context)

    return render(request, "login.html", context=context)


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

        # Field checks
        if User.objects.filter(username=email).exists():
            errors["email"] = "Email already in use"
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match"

        # Register user
        if not errors:
            user = User.objects.create_user(
                username=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, "Account succesfully created")
            return redirect("/login/")
        else:
            context["form"] = {
                "email": email,
                "password": password,
                "confirm_password": confirm_password,
                "first_name": first_name,
                "last_name": last_name,
            }
            messages.error(request, "Something went wrong")

    return render(request, "register.html", context)


@login_required(login_url='/login/')
def dashboard(request):
    context = {}

    # Projects
    projects = Project.objects.filter(
        participation__user=request.user
    )
    context["projects"] = projects

    # Render
    return render(request, "dashboard.html", context=context)


@login_required(login_url='/login/')
def add_project(request):
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        user_emails = request.POST.getlist("user")
        picture = request.FILES["picture"]

        # Get users
        users = []
        user_errors = []
        for user_email in user_emails:
            user_error = ""
            user = User.objects.filter(username=user_email).first()
            # Error
            user_error = ""
            if not user:
                user_error = "Invalid email"
            user_errors.append(user_error)
            users.append(user)
        
        # Error handling
        if "Invalid email" in user_errors:
            errors["users"] = user_errors
        if not errors:
            # Add project
            project = Project.objects.create(
                name=name,
                description=description,
                picture=picture
            )
            project.save()

            # Add creator
            participation = Participation.objects.create(
                user=request.user,
                project=project,
                role="project_manager"
            )
            participation.save()

            # Add other participations
            for user in users:
                participation = Participation.objects.create(
                    user=user,
                    project=project,
                    role="developer"
                )
                participation.save()

            messages.success(request, "Project succesfully created")
            return redirect("/dashboard/")
        else:
            context["form"] = {
                "name": name,
                "description": description,
                "users": user_emails
            }
            messages.error(request, "Something went wrong")

    return render(request, "add_project.html", context=context)


@login_required(login_url='/login/')
def project(request, pk):
    context = {}

    # Project
    project = Project.objects.filter(id=pk).first()
    context["project"] = project

    # Participation
    participation = Participation.objects.filter(
        project=project,
        user=request.user
    ).first()
    if not participation:
        messages.error(request, "Access denied")
        redirect("/dashboard/")
    
    # Role
    role = participation.role
    context["role"] = role

    return render(request, "project.html", context=context)
