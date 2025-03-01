from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.home,                          name = 'index'),
    path('login/',                         views.loginUser,                     name = 'login'),
    path('register/',                      views.registerPage,                  name = 'register'),
    path('logout/',                        views.logoutUser,                    name = 'logout'),
    path('home/',                          views.homePage,                      name = 'homePage'),
    path("create-test/",                   views.create_test,                   name="create_test"),
    path('add-questions',                  views.adding_questions,              name = 'add_questions'),
    path('batches/',                       views.batches,                       name = 'batches'),
    path('batches/delete/<int:batch_id>/', views.delete_batch,                  name='delete_batch'),
    path('courses/',                       views.courses,                       name = 'courses'),
    path('courses/delete/<int:course_id>/',views.delete_course,                 name='delete_course'),
    path('students/',                      views.students,                      name = 'students'),
]