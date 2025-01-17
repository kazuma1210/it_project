from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .models import Comment, Thread

urlpatterns = [
    # ユーザー関連のURL
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    # パスワードリセット関連
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # その他のビュー
    path('mypage/', views.mypage, name='mypage'),
    path('community_thread/', views.community_thread, name='community_thread'),
    path('save_profile/', views.save_profile, name='save_profile'),

    # スレッド作成用URL
    # urls.pyでの修正
    # urls.py
    path('create-thread/', views.create_thread, name='create-thread'),
    path('comment/<int:thread_id>/', views.comment, name='comment'),
    path('comment/<int:thread_id>/post/', views.post_comment, name='post_comment'),
    path('api/threads/', views.get_threads_by_category, name='get_threads_by_category'),
    path('comment/<int:thread_id>/', views.comment, name='comment'),
    path('password-reset/', views.password_reset_email, name='password_reset_email'),
    path('verify-email/', views.verify_email, name='verify_email'),
    # パスワードリセット画面
    path('reset-password/', views.reset_password, name='reset_password'),


    path(
        'report/comment/<int:comment_id>/',
        views.report_item,
        {'model': Comment, 'report_field': 'comment'},  # 追加引数
        name='report_comment'
    ),
    # スレッド報告
    path(
        'report/thread/<int:thread_id>/',
        views.report_item,
        {'model': Thread, 'report_field': 'thread'},  # 追加引数
        name='report_thread'
    ),
    path('api/get_user_report_data/', views.get_user_report_data, name='get_user_report_data'),

    path('profile/<int:user_id>/', views.other_user_profile, name='other_user_profile'),



    path('self_analysis/', views.self_analysis, name='self_analysis'),
    path('result_analysis/', views.result_analysis, name='result_analysis'),
    path('submit_analysis/', views.suggest_qualifications, name='submit_analysis'),
    path('delete-account/', views.delete_account, name='delete_account'),

#------------------------------管理者サイド------------------------------------
    path('custom-admin/login/', views.admin_login, name='admin_login'),
    path('admin/community_thread/', views.admin_community_thread, name='admin_community_thread'),
    path('admin/comment/<int:thread_id>/', views.admin_comment, name='admin_comment'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/user_list/', views.admin_user_list, name='admin_user_list'),
    path('admin/report_list/', views.admin_report_list, name='admin_report_list'),
    path('api/threads/sort_by_report_count/', views.get_threads_sorted_by_report_count, name='sort_by_report_count'),
    path('api/threads/sort_by_comment_report_count/', views.get_threads_sorted_by_comment_report_count, name='sort_by_comment_report_count'),
    path('api/admin/threads/', views.get_admin_threads, name='get_admin_threads')
]