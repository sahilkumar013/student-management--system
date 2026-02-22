from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student
from django.core.paginator import Paginator


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'students/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
# def student_list(request):
#     students = Student.objects.all()
#     return render(request, 'students/list.html', {'students': students})



def student_list(request):
    query = request.GET.get('q')

    if query:
        students_list = Student.objects.filter(name__icontains=query)
    else:
        students_list = Student.objects.all()

    paginator = Paginator(students_list, 5)  # 5 per page
    page = request.GET.get('page')
    students = paginator.get_page(page)

    return render(request, 'students/list.html', {'students': students})

@login_required
def add_student(request):
    if request.method == 'POST':

         
        email = request.POST['email']

        # 🔎 unique email check
        if Student.objects.filter(email=email).exists():
            return render(request, 'students/add.html', {
                'error': 'This email already exists'
            })

        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],

            
            course=request.POST['course'],
            fees=request.POST['fees'],
            is_paid='is_paid' in request.POST
        )
        return redirect('/')
    return render(request, 'students/add.html')

@login_required
def edit_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.course = request.POST['course']
        student.fees = request.POST['fees']
        student.is_paid = 'is_paid' in request.POST
        student.save()
        return redirect('/')
    return render(request, 'students/edit.html', {'student': student})

@login_required
def delete_student(request, id):
    Student.objects.get(id=id).delete()
    return redirect('/')


