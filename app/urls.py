from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # 1_user
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout_confirm/', views.logout_confirm, name='logout_confirm'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('self_analysis/', views.self_analysis, name='self_analysis'),
    path('result_analysis/', views.result_analysis, name='result_analysis'),
    path('register/', views.register, name='register'),
    path('community_thread/', views.community_thread, name='community_thread'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    

    # 2_admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/user_list/', views.user_list, name='user_list'),
    path('admin/thread_view/', views.thread_view, name='thread_view'),
]
