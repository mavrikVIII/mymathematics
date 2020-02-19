from django.urls import path
from . import views

app_name = 'mathem'

urlpatterns = [
    path('<int:question_id>/',views.detail, name='detail'),
    path('<int:question_id>/leave_answer/',views.leave_answer, name='leave_answer'),
    path('addtask',views.add_task, name='add_task'),
    path('addtask/task_add_in',views.task_add_in, name='task_add_in'),
    path('<int:question_id>/change_question/',views.change_question, name='change_question'),
    path('<int:question_id>/save_edit_question',views.save_edit_question,name='save_edit_question'),
    path('<int:question_id>/leave_comment/',views.leave_comment,name = 'leave_comment'),
    path('<int:question_id>/report_error/', views.report_error, name = 'report_error'),
    path('<int:question_id>/views_errors/', views.views_errors, name = 'views_errors'),
    path('profile', views.see_profile, name = 'see_profile'),




]
