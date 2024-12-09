from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.home, name='home'),  # ホーム画面の表示
    path('self_analysis/', views.self_analysis, name='self_analysis'),  # 自己分析開始
    path('community_thread/', views.community_thread, name='community_thread'),  # コミュニティフォーラム
    path('mypage/', views.mypage, name='mypage'),  # マイページ
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]
