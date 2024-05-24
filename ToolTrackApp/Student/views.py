from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# use auth login from django

from .models import Student

def login(request):
    if request.method == 'POST':
        studentId = request.POST.get('studentId')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(studentId=studentId)
        except Student.DoesNotExist:
            # JavaScript alert error message pop up, u can show it through {error}
            return render(request, 'login.html', {'error': 'Invalid ID'})

        # password
        if check_password(password, student.password):
            # login
            login(request, student)
            # / will be mainpage

            return redirect('/') 
        else:
            # JavaScript alert error message pop up, u can show it through {error}
            return render(request, 'login.html', {'error': 'Invalid password'})
    else:
        return HttpResponse("Method not allowed", status=405)

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
        # Add logic to handle signup, such as creating a new user
        return JsonResponse({"message": "Sign up successful"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

