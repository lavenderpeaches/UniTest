from django.contrib.auth.models     import User
from django.shortcuts               import render, redirect
from django.http                    import HttpResponse
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.urls                    import reverse_lazy
from .forms                         import testForm, batchForm, courseForm
from .models                        import Test, Batch, Course,Question, Choice
from django.shortcuts               import get_object_or_404

# Create your views here.

def home(request):
    return render(request,'index.html')

def loginUser(request):
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

    return render(request, 'index.html')
    

def registerPage(request):
    page = 'register'
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

    return render(request, 'index.html', {'page': page})

@login_required
def logoutUser(request):
    logout(request)
    return redirect(reverse_lazy('index'))

@login_required
def homePage(request):
    return render(request,'homePage.html')

@login_required
def create_test(request):
    if request.method == 'POST':
        form = testForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_question', test_id=form.instance.id)  
    else:
        form = testForm()

    return render(request, 'create_test.html', {'form': form})

@login_required
def add_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    total_questions = test.total_questions

    if request.method == 'POST':
        for i in range(1, total_questions + 1):
            question_text = request.POST.get(f'question_{i}')
            question_marks = request.POST.get(f'question_marks_{i}', 0)
            question_marks = int(question_marks) if question_marks.isdigit() else 0
            num_choices = request.POST.get(f'num_choices_{i}', 4)
            num_choices = int(num_choices) if num_choices.isdigit() else 4

            if question_text:
                question = Question.objects.create(test=test, text=question_text, marks=question_marks)

                for j in range(1, num_choices + 1):
                    choice_text = request.POST.get(f'choice_{i}_{j}')
                    is_correct = request.POST.get(f'is_correct_{i}_{j}') == 'on' 

                    if choice_text:
                        Choice.objects.get_or_create(
                            question=question, text=choice_text,
                            defaults={'is_correct': is_correct}
                        )

        return redirect('view_test', test_id=test.id)  

    return render(request, 'addQuestion.html', {'test': test, 'total_questions': range(1, total_questions + 1)})

@login_required
def view_test(request, test_id):
    test      = get_object_or_404(Test, id=test_id)
    questions = test.questions.all() 
    choices   = Choice.objects.filter(question__in=questions)  
    batch     = test.batch
    course    = test.course
    context = {
        'test'      : test,
        'questions' : questions,
        'choices'   : choices,
        'batch'     : batch,
        'course'    : course,
    }
    return render(request, 'view_test.html', context)


@login_required
def batches(request):
    all_batches = Batch.objects.all()
    
    if request.method == "POST":
        form = batchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('batches')
        else:
            print("Form Errors:", form.errors)
    else:
        form = batchForm()
    
    context = {
                    'batches': all_batches,
                    'form': form,  
                }
    return render(request, 'batches.html', context)

def students(request):
    return render(request, 'students.html')

def courses(request):
    all_courses = Course.objects.all()

    if request.method == "POST":
        form = courseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            print("Form Errors:", form.errors)
    else:    
        form = courseForm()
    context     = {
                    'all_courses': all_courses,
                    'form': form,  
                  }
    return render(request, 'courses.html',context)

def delete_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)

    if request.method == "POST":
        batch.delete()
        return redirect('batches')  

    return render(request, 'batches.html') 

def delete_course(request,course_id):
    course = get_object_or_404(Course, id = course_id)

    if request.method == "POST":
        course.delete()
        return redirect('courses')
    
    return render(request, 'courses.html')