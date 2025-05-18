from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.home,                          name = 'index'),
    path('login/',                         views.loginUser,                     name = 'login'),
    path('register/',                      views.registerPage,                  name = 'register'),
    path('logout/',                        views.logoutUser,                    name = 'logout'),

    path('home/',                          views.homePage,                      name = 'homePage'),

    path("create-test/",                   views.create_test,                   name = 'create_test'),
    path('tests/',                         views.list_tests,                    name = 'list_tests'),
    path('tests/update/<int:test_id>/',    views.update_test,                   name = 'update_test'),
    path('tests/delete/<int:test_id>/',    views.delete_test,                   name = 'delete_test'),
    path("add-question/<int:test_id>/",    views.add_question,                  name = 'add_question'),
    path('view-test/<int:test_id>/',       views.view_test,                     name = 'view_test'),
    path('update-test/<int:test_id>/',     views.update_test,                   name = 'update_test'),
    path('batches/',                       views.batches,                       name = 'batches'),
    path('batches/update/<int:batch_id>/', views.update_batch,                  name = 'update_batch'),
    path('batches/delete/<int:batch_id>/', views.delete_batch,                  name = 'delete_batch'),
    path('batches/<int:batch_id>/students/', views.view_batch_students,         name = 'view_batch_students'),
    path('batches/<int:batch_id>/import-students/', views.import_students,      name = 'import_students'),
    path('delete-student/<int:student_id>/', views.delete_student,              name = 'delete_student'),
    path('courses/',                       views.courses,                       name = 'courses'),
    path('courses/delete/<int:course_id>/',views.delete_course,                 name = 'delete_course'),
    path('update-course/<int:course_id>/', views.update_course,                 name = 'update_course'),

    path('students/',                      views.students,                      name = 'students'),
    path('test/<int:test_id>/generate-codes/', views.generate_test_codes,       name='generate_test_codes'),
    path('enter-test-code/',                    views.enter_test_code,          name='enter_test_code'),
    path('take-test/<int:attempt_id>/',         views.take_test,                name='take_test'),
    path('reports/',                            views.reports,                  name='reports'),
    path('attempt/<int:attempt_id>/',           views.view_attempt,             name='view_attempt'),
]