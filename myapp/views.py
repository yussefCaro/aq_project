from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import Project
from .forms import CreateNewProject, TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    title = 'Hello, Django!'
    return render(request, 'index.html', {
        'title': title
    })


def about(request):
    username = 'Yussef'
    return render(request, 'about.html', {
        'username': username})

@login_required
def projects(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/projects.html', {
        'projects': projects
    })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:  # validation error
            return render(request, 'tasks/create_task.html', {
                'form': TaskForm,
                'error': 'Bad data passed in'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/task_detail.html', {
                'form': form,
                'error': 'Error updating task'
            })

@login_required
def tasks_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(
            name=request.POST['name'],
            user=request.user
        )
        return redirect('projects')


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'GET':
        tasks = Task.objects.filter(project_id=project_id)
        form = CreateNewProject(instance=project)
        return render(request, 'projects/project_detail.html', {
            'project': project,
            'tasks': tasks,
            'form': form
        })

    elif request.method == 'POST':
        form = CreateNewProject(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('projects')  # Puedes agregar un mensaje de éxito con mensajes Django
        else:
            tasks = Task.objects.filter(project_id=project_id)
            return render(request, 'projects/project_detail.html', {
                'project': project,
                'tasks': tasks,
                'form': form,
                'error': 'Error updating project. Please check the form.'
            })
