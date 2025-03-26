from django.urls import path
from .views import signup,login_and_get_employee,employee_dashboard,home

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_and_get_employee, name='login_and_get_employee'),
      path('employee/home/<str:employee_id>/', employee_dashboard, name='employee_dashboard'),
      path('home/',home,name='home'),
]
