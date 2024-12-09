from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.home, name='home'),  # ホーム画面
    path('self_analysis/', views.self_analysis, name='self_analysis'),
    path('result_analysis/', views.result_analysis, name='result_analysis'),
    path('community_thread/', views.community_thread, name='community_thread'),
    path('mypage/', views.mypage, name='mypage'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup, name='signup'),  # サインアップページ
    path('verify_email/<str:token>/', views.verify_email, name='verify_email'),  # メール認証ページ
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  # アカウント有効化URL
]
