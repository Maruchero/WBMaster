from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils.html import escape

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


def docs_models(request):
    return render(request, "docs_models.html")

def docs_urls(request):
    return render(request, "docs_urls.html")

def docs_views(request):
    return render(request, "docs_views.html")

def docs_templates(request):
    return render(request, "docs_templates.html")

def logout(request):
    user_logout(request)
    messages.success(request, "Disconnesso con successo")
    return redirect("/")


def login(request):
    # Context
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        email = escape(request.POST["email"])
        password = escape(request.POST["password"])

        # Login user
        user = authenticate(username=email, password=password)
        if user:
            # User is authenticated
            user_login(request, user)
            messages.success(request, "Accesso effettuato con successo")
            return redirect("/dashboard/", context=context)
        else:
            context["form"] = {
                "email": email,
                "password": password,
            }
            messages.error(request, "Credenziali errate")
            errors["credentials"] = "Credenziali errate"
            return render(request, "login.html", context=context)

    return render(request, "login.html", context=context)


def register(request):
    # Context
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        email = escape(request.POST["email"])
        password = escape(request.POST["password"])
        confirm_password = escape(request.POST["confirm_password"])
        first_name = escape(request.POST["first_name"])
        last_name = escape(request.POST["last_name"])

        # Field checks
        if User.objects.filter(username=email).exists():
            errors["email"] = "Email già in uso"
        if password != confirm_password:
            errors["confirm_password"] = "Le password non corrispondono"

        # Register user
        if not errors:
            user = User.objects.create_user(
                username=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, "Account creato con successo")
            return redirect("/login/")
        else:
            context["form"] = {
                "email": email,
                "password": password,
                "confirm_password": confirm_password,
                "first_name": first_name,
                "last_name": last_name,
            }
            messages.error(request, "Qualcosa è andato storto")

    return render(request, "register.html", context)


@login_required(login_url='/login/')
def dashboard(request):
    context = {}

    # Projects
    projects = Project.objects.filter(
        participation__user=request.user
    )
    context["projects"] = projects

    for project in projects:

        # Participation
        participation = Participation.objects.filter(
            project=project,
            user=request.user
        ).first()
        if not participation:
            messages.error(request, "Non hai i permessi per accedere a questo progetto")
            return redirect("/dashboard/")

        # Role
        role = participation.role
        project.role = role

    # Render
    return render(request, "dashboard.html", context=context)


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
        messages.error(request, "Non hai i permessi per accedere a questo progetto")
        return redirect("/dashboard/")

    # Role
    role = participation.role
    context["role"] = role

    # Tasks
    tasks = Task.objects.filter(project=project).order_by("start")
    context["tasks"] = tasks

    # Assignments
    for task in tasks:
        assignment = Assignment.objects.filter(task=task).first()
        if assignment:
            task.assignment = assignment.user

    # Form
    formdata = request.session.get("form", False)
    if formdata:
        context["form"] = formdata
    
    # Errors
    errors = request.session.get("errors", False)
    if errors:
        context["errors"] = errors
    
    # Empty session
    if formdata:
        del request.session["form"]
    if errors:
        del request.session["errors"]

    return render(request, "project.html", context=context)


@login_required(login_url='/login/')
def add_task(request):
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        project_id = escape(request.POST["project"])
        if "parent_task" in request.POST:
            parent_task = escape(request.POST["parent_task"])
        else:
            parent_task = None
        name = escape(request.POST["name"])
        description = escape(request.POST["description"])
        start = escape(request.POST["start"])
        end = escape(request.POST["end"])
        color = request.POST["color"]
        user_email = escape(request.POST["user"])

        # Project
        project = Project.objects.filter(id=project_id).first()
        if not project:
            messages.error(request, "Progetto non trovato")
            return redirect(f"/dashboard/")
            
        # Check user permissions
        participation = Participation.objects.filter(
            project=project,
            user=request.user
        ).first()
        if not participation or participation.role != "project_manager":
            messages.error(request, "Non hai i permessi per modificare questo progetto")
            return redirect(f"/projects/{project_id}/")

        # Get user
        if user_email:
            user = User.objects.filter(username=user_email).first()

        # Data checks
        if user_email and not user:
            errors["users"] = "Email non valida"
        if start > end:
            errors["start"] = "La data di inizio deve precedere la data di fine"

        if not errors:
            # Add task
            task = Task.objects.create(
                project=project,
                parent_task_id=parent_task,
                name=name,
                description=description,
                start=start,
                end=end,
                color=color,
            )
            task.save()

            # Assign task to
            if user_email:
                assignment = Assignment.objects.create(
                    task=task,
                    user=user,
                )
                assignment.save()

            messages.success(request, "Task aggiunta con successo")
        else:
            parent = Task.objects.filter(
                id=parent_task).first() if parent_task else None
            request.session["form"] = {
                "mode": "Add",
                "project": project_id,
                "parent_id": parent_task,
                "parent_name": parent.name if parent else None,
                "name": name,
                "description": description,
                "start": start,
                "end": end,
                "color": color,
            }
            request.session["errors"] = errors
            messages.error(request, "Qualcosa è andato storto")
        return redirect(f"/projects/{project_id}/")


@login_required(login_url='/login/')
def edit_task(request, pk):
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        project_id = escape(request.POST["project"])
        if "parent_task" in request.POST:
            parent_task = escape(request.POST["parent_task"])
        else:
            parent_task = None
        name = escape(request.POST["name"])
        description = escape(request.POST["description"])
        start = escape(request.POST["start"])
        end = escape(request.POST["end"])
        color = request.POST["color"]
        user_email = escape(request.POST["user"])

        # Project
        project = Project.objects.filter(id=project_id).first()
        if not project:
            messages.error(request, "Progetto non trovato")
            return redirect(f"/dashboard/")

        # Check user permissions
        participation = Participation.objects.filter(
            project=project,
            user=request.user
        ).first()
        if not participation or participation.role != "project_manager":
            messages.error(request, "Non hai i permessi per modificare questo progetto")
            return redirect(f"/projects/{project_id}/")

        # Get user
        if user_email:
            user = User.objects.filter(username=user_email).first()

        # Data checks
        if user_email and not user:
            errors["users"] = "Email non valida"
        if start > end:
            errors["start"] = "La data di inizio deve precedere la data di fine"

        if not errors:
            # Get task
            task = Task.objects.filter(id=pk).first()
            if not task:
                messages.error(request, "Task non trovata")
                return redirect(f"/projects/{project_id}/")

            # Edit task
            task.name = name
            task.description = description
            task.start = start
            task.end = end
            task.color = color
            task.save()

            # Remove and add assignments
            if user_email:
                assignments = Assignment.objects.filter(task=task)
                for assignment in assignments:
                    if assignment.user != user:
                        assignment.delete()
                assignment = Assignment.objects.filter(
                    task=task,
                    user=user,
                ).first()
                if not assignment:
                    assignment = Assignment.objects.create(
                        task=task,
                        user=user,
                    )
                    assignment.save()

            messages.success(request, "Task aggiornata con successo")
        else:
            parent = Task.objects.filter(id=parent_task).first()
            request.session["form"] = {
                "mode": "Edit",
                "project": project_id,
                "parent_id": parent_task,
                "parent_name": parent.name if parent else None,
                "name": name,
                "description": description,
                "start": start,
                "end": end,
                "color": color,
            }
            request.session["errors"] = errors
            messages.error(request, "Aggiornamento task non riuscito")
        return redirect(f"/projects/{project_id}/")


@login_required(login_url='/login/')
def delete_task(request, pk):
    # Get task
    task = Task.objects.filter(id=pk).first()
    if not task:
        messages.error(request, "Task non trovata")
        return redirect("/dashboard/")

    # Project
    project = Project.objects.filter(id=task.project_id).first()
    if not project:
        messages.error(request, "Progetto non trovato")
        return redirect("/dashboard/")

    # Check user permissions
    participation = Participation.objects.filter(
        project=project,
        user=request.user
    ).first()
    if not participation or participation.role != "project_manager":
        messages.error(request, "Non hai i permessi per modificare questo progetto")
        return redirect(f"/projects/{task.project_id}/")

    task.delete()

    messages.success(request, "Task eliminata con successo")
    return redirect(f"/projects/{task.project_id}/")


@login_required(login_url='/login/')
def add_project(request):
    context = {}
    errors = {}
    context["errors"] = errors

    # If the form has been submitted
    if request.method == "POST":
        name = escape(request.POST["name"])
        description = escape(request.POST["description"])
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
                user_error = "Email non valida"
            if user_email == request.user.username:
                user_error = "Non puoi aggiungere il tuo account"
            user_errors.append(user_error)
            users.append(user)

        # Error handling
        if any(error != "" for error in user_errors):
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

            messages.success(request, "Progetto creato con successo")
            return redirect("/dashboard/")
        else:
            context["form"] = {
                "name": name,
                "description": description,
                "users": user_emails
            }
            messages.error(request, "Qualcosa è andato storto")

    return render(request, "add_project.html", context=context)


@login_required(login_url='/login/')
def edit_project(request, pk):
    context = {}
    errors = {}
    context["errors"] = errors
    context["mode"] = "edit"

    # Project
    project = Project.objects.filter(id=pk).first()
    if not project:
        messages.error(request, "Progetto non trovato")
        return redirect("/dashboard/")

    # Check user permissions
    participation = Participation.objects.filter(
        project=project,
        user=request.user
    ).first()
    if not participation or participation.role != "project_manager":
        messages.error(request, "Non hai i permessi per modificare questo progetto")
        return redirect("/dashboard/")

    # Edit
    if request.method == "POST":
        name = escape(request.POST["name"])
        description = escape(request.POST["description"])
        user_emails = request.POST.getlist("user")

        # Get users
        users = []
        user_errors = []
        for user_email in user_emails:
            user_error = ""
            user = User.objects.filter(username=user_email).first()
            # Error
            user_error = ""
            if not user:
                user_error = "Email non valida"
            user_errors.append(user_error)
            users.append(user)

        # Error handling
        if "Email non valida" in user_errors:
            errors["users"] = user_errors
        if not errors:
            # Edit project
            project.name = name
            project.description = description
            project.save()

            # Remove and add participations
            participations = Participation.objects.filter(
                project=project).exclude(user=request.user)
            for participation in participations:
                if not participation.user in users:
                    participation.delete()
            for user in users:
                participation = Participation.objects.filter(
                    project=project, user=user).first()
                if not participation:
                    participation = Participation.objects.create(
                        user=user,
                        project=project,
                        role="developer"
                    )
                    participation.save()

            messages.success(request, "Progetto aggiornato con successo")
            return redirect("/dashboard/")

        messages.error(request, "Qualcosa è andato storto")
        return render(request, "add_project.html", context=context)

    # Participators + form
    users = User.objects.filter(
        participation__project=project).exclude(id=request.user.id)
    context["form"] = {
        "project_id": pk,
        "name": project.name,
        "description": project.description,
        "users": [user.username for user in users]
    }

    return render(request, "add_project.html", context=context)


@login_required(login_url='/login/')
def delete_project(request, pk):
    # Get project
    project = Project.objects.filter(id=pk).first()
    if not project:
        messages.error(request, "Progetto non trovato")
        return redirect("/dashboard/")

    # Check user permissions
    participation = Participation.objects.filter(
        project=project,
        user=request.user
    ).first()
    if not participation or participation.role != "project_manager":
        messages.error(request, "Non hai i permessi necessari")
        return redirect(f"/dashboard/")

    project.delete()

    messages.success(request, "Progetto eliminato con successo")
    return redirect(f"/dashboard/")
