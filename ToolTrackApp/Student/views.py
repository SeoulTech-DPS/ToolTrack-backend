from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

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





def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 사용자가 입력한 정보에서 username, password 추출
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            studentId = request.POST.get('studentId')
            
            # 새로운 Student 객체 생성
            student = Student.objects.create(
                studentId=studentId,
                username=username,
                password=password
            )
            
            # login
            login(request, student)
            
            # redirect to main
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, '/SignUp.html', {'form': form})
