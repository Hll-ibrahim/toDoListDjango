import json

from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from task.models import Task, Category


def index(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        data = serializers.serialize("json", tasks)
        return JsonResponse({"success": True, 'tasks': data})


@csrf_exempt
def create(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            Task.objects.get(title=data['title'])
        except:
            title = data['title']
            description = data['description']
            done = data['done']
            try:
                category = Category.objects.get(id=data['category'])
            except Category.DoesNotExist:
                return JsonResponse({'success': False, "message": "Category does not exist"})
            task = Task(title=title, description=description, done=done, category_id=category.id)
            task.save()
            return JsonResponse({"success": True, "data": task.title, "id": task.id})
        else:
            return JsonResponse({'success': False, "message": "Task title already exists"})


@csrf_exempt
def delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        id = data['id']
        task = Task.objects.get(id=id)
        task.delete()
        return JsonResponse({"success": True, "data": task.title})


@csrf_exempt
def update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        title = data['title']
        description = data['description']
        done = data['done']
        task = Task.objects.get(id=data['id'])
        task.title = title
        task.description = description
        task.done = done
        try:
            category = Category.objects.get(id=data['category'])
            task.category_id = category.id
        except:
            return JsonResponse({'success': False, "message": "Category does not exist"})
        try:
            task.save()
            return JsonResponse({"success": True, "data": title})
        except:
            return JsonResponse({"success": False, "message": "Task title already exists"})
