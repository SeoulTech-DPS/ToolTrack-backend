from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# use auth login from django

from .models import Student

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    print("Entered")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            studentId = data.get('studentId')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        try:
            student = Student.objects.get(studentId=studentId)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Invalid ID'}, status=400)

        if check_password(password, student.password):
            login(request, student)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.http import JsonResponse
import json

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        data = json.loads(request.body)
        student_id = data['studentId']
        username = data['username']
        password = data['password']

        # Check if the username or studentId already exists
        if Student.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        if Student.objects.filter(studentId=student_id).exists():
            return JsonResponse({"error": "Student ID already exists"}, status=400)

        # Create and save the new student
        student = Student(
            studentId=student_id,
            name='',  # Assuming name is not provided in the request
            username=username,
            password=password  # Save the password as plain text (not recommended)
        )
        student.save()

        return JsonResponse({"message": "Sign up successful"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def getTestResponse(request):
    return JsonResponse({"message":"Sign up successful"})
