from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import Project, Task
from .forms import CreateNewProject, TaskForm
from .models import Task


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


def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {
        'projects': projects
    })


def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })


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
            form.save()
            return redirect('tasks')
        except ValueError:  # validation error
            return render(request, 'tasks/create_task.html', {
                'form': TaskForm,
                'error': 'Bad data passed in'
            })


def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })


def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(
            name=request.POST['name'],
        )
        return redirect('projects')


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks
    })
