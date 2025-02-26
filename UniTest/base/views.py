from django.contrib.auth.models     import User
from django.shortcuts               import render,redirect
from django.http                    import HttpResponse
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.urls                    import reverse_lazy
from .forms                         import testForm
# Create your views here.

def home(request):
    return render(request,'index.html')

def loginUser(request):
    page = 'login'
    user = None
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('homePage')
    else:
        messages.error(request, "Wrong username or password. Please try again.")

    return render(request, 'index.html', {'page': page})
    

def registerPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        print(email,username,password,password2)

        if password != password2:
            messages.error(request, "Password do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.username = user.username.lower()
        user.save()
        
        login(request, user)

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('homePage')

    return render(request, 'index.html')

@login_required
def logoutUser(request):
    logout(request)
    return redirect(reverse_lazy('index'))

@login_required
def homePage(request):
    return render(request,'homePage.html');

@login_required
def create_test(request):
    form = testForm()
    return render(request, 'create_test.html',{'form':form})
