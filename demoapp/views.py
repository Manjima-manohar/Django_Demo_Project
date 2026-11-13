from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile,Department,Employee,Project
# Create your views here.

def index(request):
    return render(request,"index.html")


def register(request):
    if request.method == "POST":
            username = request.POST.get("username")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            if password1 == password2:
    
                user=User.objects.create_user(
                    username=username,
                    password=password1
                )
                UserProfile.objects.create(
                    user=user,
                    phone=phone,
                    address=address
                )
                return redirect("login")
    return render(request, "register.html")




def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate( request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


@login_required(login_url="login")
def about(request):
    dept=Department.objects.all()
    projects = Project.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        address=request.POST.get("address")
        department=request.POST.get("department")
        project = request.POST.getlist("projects")
        emp=Employee.objects.create(name=name,address=address,department_id=department)
        emp.projects.set(project)
        emp.save()
        return redirect("index")
    return render(request,"about.html",{"dept":dept,"projects": projects})

@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def display_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request,"profile.html",{"profile": profile})

# python manage.py makemigrations-user,session
# python manage.py migrate