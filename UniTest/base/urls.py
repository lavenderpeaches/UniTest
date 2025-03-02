from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.home,                          name = 'index'),
    path('login/',                         views.loginUser,                     name = 'login'),
    path('register/',                      views.registerPage,                  name = 'register'),
    path('logout/',                        views.logoutUser,                    name = 'logout'),
    path('home/',                          views.homePage,                      name = 'homePage'),
    path("create-test/",                   views.create_test,                   name = 'create_test'),
    path("add-question/<int:test_id>/",    views.add_question,                  name = 'add_question'),
    path('view-test/<int:test_id>/',       views.view_test,                    name = 'view_test'),
    path('batches/',                       views.batches,                       name = 'batches'),
    path('batches/delete/<int:batch_id>/', views.delete_batch,                  name = 'delete_batch'),
    path('courses/',                       views.courses,                       name = 'courses'),
    path('courses/delete/<int:course_id>/',views.delete_course,                 name = 'delete_course'),
    path('students/',                      views.students,                      name = 'students'),
]