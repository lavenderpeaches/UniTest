from django.contrib.auth.models     import User
from django.shortcuts               import render, redirect
from django.http                    import HttpResponse, JsonResponse
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.urls                    import reverse_lazy
from .forms                         import testForm, batchForm, courseForm, StudentImportForm
from .models                        import Test, Batch, Course,Question, Choice, TestCode, TestAttempt, Answer, Student
from django.shortcuts               import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
import csv
import io
from django.http import HttpResponseForbidden

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

    return render(request, 'login.html')
    

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
            test = form.save()
            # Parse questions and choices from POST data
            total_questions = int(request.POST.get('total_questions', 1))
            for i in range(1, total_questions + 1):
                question_text = request.POST.get(f'question_{i}')
                question_marks = request.POST.get(f'question_marks_{i}', 0)
                question_marks = int(question_marks) if str(question_marks).isdigit() else 0
                num_choices = request.POST.get(f'num_choices_{i}', 4)
                num_choices = int(num_choices) if str(num_choices).isdigit() else 4
                if question_text:
                    question = Question.objects.create(test=test, text=question_text, marks=question_marks, num_choices=num_choices)
                    for j in range(1, num_choices + 1):
                        choice_text = request.POST.get(f'choice_{i}_{j}')
                        is_correct = request.POST.get(f'is_correct_{i}_{j}') == 'on'
                        if choice_text:
                            Choice.objects.create(
                                question=question, text=choice_text,
                                is_correct=is_correct
                            )
            return redirect('view_test', test_id=test.id)
    else:
        form = testForm()
    return render(request, 'create_test.html', {'form': form})

@login_required
def add_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    total_questions = test.total_questions

    if request.method == 'POST':
        from django.http import HttpResponse
        return HttpResponse("POST received in add_question view!")  # TEMP DEBUG
        print(f"Processing {total_questions} questions for test {test.id}")
        for i in range(1, total_questions + 1): 
            question_text = request.POST.get(f'question_{i}')
            question_marks = request.POST.get(f'question_marks_{i}', 0)
            question_marks = int(question_marks) if question_marks.isdigit() else 0
            num_choices = request.POST.get(f'num_choices_{i}', 4)
            num_choices = int(num_choices) if num_choices.isdigit() else 4

            print(f"Question {i}: text='{question_text}', marks={question_marks}, num_choices={num_choices}")

            if question_text:
                question = Question.objects.create(test=test, text=question_text, marks=question_marks)
                print(f"Created question {question.id}")

                for j in range(1, num_choices + 1):
                    choice_text = request.POST.get(f'choice_{i}_{j}')
                    is_correct = request.POST.get(f'is_correct_{i}_{j}') == 'on' 

                    print(f"Choice {j}: text='{choice_text}', is_correct={is_correct}")

                    if choice_text:
                        choice = Choice.objects.create(
                            question=question, text=choice_text,
                            is_correct=is_correct
                        )
                        print(f"Created choice {choice.id}")

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

@login_required
def import_students(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    
    if request.method == 'POST':
        form = StudentImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            
            for row in reader:
                try:
                    Student.objects.create(
                        batch=batch,
                        name=row['Name'],
                        email=row['Email'],
                        roll_number=row['Roll Number']
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    messages.error(request, f"Error importing student {row.get('Name', 'Unknown')}: {str(e)}")
            
            messages.success(request, f"Successfully imported {success_count} students. Failed to import {error_count} students.")
            return redirect('view_batch_students', batch_id=batch_id)
    else:
        form = StudentImportForm()
    
    return render(request, 'import_students.html', {
        'form': form,
        'batch': batch
    })

@login_required
def view_batch_students(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    students = batch.students.all().order_by('roll_number')
    
    return render(request, 'view_batch_students.html', {
        'batch': batch,
        'students': students
    })

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
    context = {
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

@login_required
def update_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    
    if request.method == "POST":
        form = batchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch updated successfully!")
            return redirect('batches')
    else:
        form = batchForm(instance=batch)
    
    return render(request, 'update_batch.html', {
        'form': form,
        'batch': batch
    })

def delete_course(request, course_id):
    course = get_object_or_404(Course, id = course_id)

    if request.method == "POST":
        course.delete()
        return redirect('courses')
    
    return render(request, 'courses.html')

def update_course(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = courseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            return redirect('courses')
    else:   
        form = courseForm(instance=course)

    return render(request, 'update_course.html', {'course': course, 'form':form})

@login_required
def list_tests(request):
    tests = Test.objects.all()
    return render(request, 'list_tests.html', {'tests': tests})

@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == "POST":
        test.delete()
        return redirect('list_tests')
    
    return render(request, 'list_tests.html')

@login_required
def update_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()
    
    if request.method == 'POST':
        print("Request body: ",request.body)
        print("UTG|F-8 ",request.body.decode('utf-8'))
        print(request.headers.get('Content-Type'))
        print(request.META["Content-Type"])
        form = testForm(request.POST, instance=test)
        print("Form Data:", request.POST)
        print("Form Errors:", form.errors)

        if form.is_valid():
            form.save()

            # Update questions and choices
            for question in questions:
                question_text = request.POST.get(f"question_{question.id}")
                question_marks = request.POST.get(f"question_marks_{question.id}")
                question.text = question_text
                question.marks = question_marks
                question.save()

                for choice in question.choices.all():
                    choice_text = request.POST.get(f"choice_{question.id}_{choice.id}")
                    is_correct = request.POST.get(f"is_correct_{question.id}_{choice.id}") is not None
                    choice.text = choice_text
                    choice.is_correct = is_correct
                    choice.save()

            return redirect('list_tests')
    else:
        form = testForm(instance=test)

    return render(request, 'update_test.html', {'form': form, 'test': test, 'questions': questions})



@require_POST
def generate_test_codes(request, test_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    test = get_object_or_404(Test, id=test_id)
    codes = TestCode.objects.filter(test=test, is_used=False)
    for code_obj in codes:
        subject = f'Test Access Code: {test.name}'
        message = f'''
        Hello {code_obj.student_name},
        
        You have been assigned a test: {test.name}
        Your access code is: {code_obj.code}
        
        Please visit the test platform and enter this code to start the test.
        This code will expire in 24 hours.
        
        Duration: {test.duration}
        Total Marks: {test.total_marks}
        
        Good luck!
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [code_obj.student_email],
            fail_silently=False,
        )
    messages.success(request, 'Test codes have been sent to students.')
    return redirect('list_tests')

def enter_test_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            test_code = TestCode.objects.get(
                code=code,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            
            # Create test attempt
            attempt = TestAttempt.objects.create(
                test=test_code.test,
                student_name=test_code.student_name,
                student_email=test_code.student_email
            )
            
            # Mark code as used
            test_code.is_used = True
            test_code.save()
            
            # Store attempt ID in session
            request.session['attempt_id'] = attempt.id
            request.session['student_name'] = attempt.student_name
            
            return redirect('take_test', attempt_id=attempt.id)
        except TestCode.DoesNotExist:
            messages.error(request, 'Invalid or expired code.')
    
    return render(request, 'enter_test_code.html')

def take_test(request, attempt_id):
    # Get attempt from session
    session_attempt_id = request.session.get('attempt_id')
    if not session_attempt_id or str(session_attempt_id) != str(attempt_id):
        messages.error(request, 'Invalid test session.')
        return redirect('enter_test_code')
    
    attempt = get_object_or_404(TestAttempt, id=attempt_id)
    
    if attempt.is_submitted:
        messages.error(request, 'You have already submitted this test.')
        return redirect('enter_test_code')
    
    if attempt.is_time_up():
        # Auto-submit the test
        attempt.end_time = timezone.now()
        attempt.is_submitted = True
        attempt.save()
        messages.error(request, 'Time is up! Your test has been auto-submitted.')
        return redirect('enter_test_code')
    
    if request.method == 'POST':
        # Save answers for each question
        for question in attempt.test.questions.all():
            choice_id = request.POST.get(f'q{question.id}')
            choice = None
            if choice_id:
                try:
                    choice = Choice.objects.get(id=choice_id)
                except Choice.DoesNotExist:
                    choice = None
            Answer.objects.create(
                attempt=attempt,
                question=question,
                choice=choice
            )
        attempt.end_time = timezone.now()
        attempt.is_submitted = True
        # Calculate score here if needed
        attempt.save()
        # Clear session
        request.session.pop('attempt_id', None)
        request.session.pop('student_name', None)
        messages.success(request, 'Test submitted successfully!')
        return redirect('enter_test_code')
    
    context = {
        'attempt': attempt,
        'test': attempt.test,
        'questions': attempt.test.questions.all(),
        'remaining_time': attempt.test.duration - (timezone.now() - attempt.start_time),
        'student_name': request.session.get('student_name')
    }
    return render(request, 'take_test.html', context)

def reports(request):
    # Only allow staff/faculty
    if not request.user.is_staff:
        return redirect('index')
    
    attempts = TestAttempt.objects.filter(is_submitted=True).order_by('-end_time')
    context = {
        'attempts': attempts,
    }
    return render(request, 'reports.html', context)

def view_attempt(request, attempt_id):
    if not request.user.is_staff:
        return redirect('index')
    attempt = get_object_or_404(TestAttempt, id=attempt_id)
    answers = attempt.answers.select_related('question', 'choice').all()
    context = {
        'attempt': attempt,
        'answers': answers,
    }
    return render(request, 'view_attempt.html', context)

@login_required
def update_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    
    if request.method == 'POST':
        # Convert duration from minutes to timedelta
        duration_minutes = request.POST.get('duration')
        if duration_minutes:
            request.POST = request.POST.copy()
            request.POST['duration'] = timedelta(minutes=int(duration_minutes))
        
        form = testForm(request.POST, instance=test)
        if form.is_valid():
            test = form.save()
            
            # Update existing questions
            for question in test.questions.all():
                question_id = str(question.id)
                question_text = request.POST.get(f'question_text_{question_id}')
                question_marks = request.POST.get(f'question_marks_{question_id}')
                num_choices = request.POST.get(f'num_choices_{question_id}')
                
                if question_text:
                    question.text = question_text
                    question.marks = int(question_marks) if question_marks else 1
                    question.num_choices = int(num_choices) if num_choices else 4
                    question.save()
                    
                    # Update choices
                    for choice in question.choices.all():
                        choice_id = str(choice.id)
                        choice_text = request.POST.get(f'choice_text_{question_id}_{choice_id}')
                        is_correct = request.POST.get(f'is_correct_{question_id}_{choice_id}') == 'on'
                        
                        if choice_text:
                            choice.text = choice_text
                            choice.is_correct = is_correct
                            choice.save()
                        else:
                            choice.delete()
            
            # Add new questions
            for key, value in request.POST.items():
                if key.startswith('question_text_new_'):
                    question_id = key.split('_')[-1]
                    question_text = value
                    question_marks = request.POST.get(f'question_marks_new_{question_id}')
                    num_choices = request.POST.get(f'num_choices_new_{question_id}')
                    
                    if question_text:
                        # Create new question
                        question = Question.objects.create(
                            test=test,
                            text=question_text,
                            marks=int(question_marks) if question_marks else 1,
                            num_choices=int(num_choices) if num_choices else 4
                        )
                        
                        # Add choices for new question
                        for i in range(1, int(num_choices) + 1):
                            choice_text = request.POST.get(f'choice_text_new_{question_id}_{i}')
                            is_correct = request.POST.get(f'is_correct_new_{question_id}_{i}') == 'on'
                            
                            if choice_text:
                                Choice.objects.create(
                                    question=question,
                                    text=choice_text,
                                    is_correct=is_correct
                                )
            
            # Update total questions and marks
            test.total_questions = test.questions.count()
            test.total_marks = sum(q.marks for q in test.questions.all())
            test.save()
            
            messages.success(request, 'Test updated successfully!')
            return redirect('list_tests')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = testForm(instance=test)
        # Convert duration to minutes for the template
        duration_minutes = int(test.duration.total_seconds() // 60)
    
    return render(request, 'update_test.html', {
        'test': test, 
        'form': form,
        'duration_minutes': duration_minutes
    })

@login_required
@require_POST
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    batch_id = student.batch.id
    
    try:
        student.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})