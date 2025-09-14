from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name='index'),
    path("home/", views.home, name='home'),
    path('report/', views.report_complaint, name='report_complaint'),
    path('assign_worker/', views.assign_worker, name='assign_worker'),
    path('resolve_complaint/', views.resolve_complaint, name='resolve_complaint'),
    path('add_department/',views.add_department, name='add_department'),
    path('departments/', views.departments, name='departments'),
    path('admin_tracking/', views.admin_track, name='admin_track'),
    path('civilian_track/', views.civilian_track, name='civilian_track'),
    path('dept_track/', views.dept_track, name='dept_track'),
    path('sub_dept/', views.sub_dept, name='sub_dept'),
    path('show_departments',views.show_departments,name='show_departments')
]