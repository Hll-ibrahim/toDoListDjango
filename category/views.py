import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from category.models import Category


# Create your views here.
def index(request):
    if request.method == 'GET':
        category = Category.objects.all()
        if category:
            data = serializers.serialize('json', category)
            return JsonResponse({"success": True, "data": data})
        return JsonResponse({"success": True, 'message': 'There is no Category!'})

@csrf_exempt
def create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']

        try:
            Category.objects.get(name=name)
        except:
            category = Category(name=name)
            category.save()
            return JsonResponse({"success": True, "data": category.name})
        else:
            return JsonResponse({"success": False, "message": "Category name already exists!", "name": name})

@csrf_exempt
def delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        category = Category.objects.get(name=data['name'])
        category.delete()
        return JsonResponse({"success": True, "data": category.name})

@csrf_exempt
def update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            category = Category.objects.get(id=data['id'])
        except:
            return JsonResponse({"success": False, "message": "There is no Category!"})
        category.name = data['name']

        try:
            category.save()
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
        return JsonResponse({"success": True})
