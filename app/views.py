from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import random

from .models import Profile, Thread, Comment
from .forms import CustomUserCreationForm, CommentForm

# カスタムユーザーモデルを使用
User = get_user_model()

# --- ユーティリティ関数 ---

def remove_duplicate_messages(request):
    storage = messages.get_messages(request)
    unique_messages = []
    unique_message_texts = set()

    for message in storage:
        if message.message not in unique_message_texts:
            unique_message_texts.add(message.message)
            unique_messages.append(message)

    storage._loaded_data = unique_messages
    storage.used = False

# パスワードリセット例
# (開発用。運用時には使用しないこと)
def reset_password_example():
    try:
        user = User.objects.get(email='craft20041210@gmail.com')
        user.set_password('kazuma0129')
        user.save()
        print("パスワードが正しくリセットされました。")
    except User.DoesNotExist:
        print("指定されたユーザーは存在しません。")

# --- ユーザー関連ビュー ---

# ホーム画面
def home(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'ゲスト',
    }
    return render(request, '1_user/ホーム/home.html', context)

# 新規登録
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password1']

            verification_code = random.randint(1000, 9999)
            request.session['verification_code'] = verification_code

            send_mail(
                '認証コードのお知らせ',
                f'以下の認証コードを入力してください: {verification_code}',
                'info001@meltfire.net',
                [form.cleaned_data['email']],
                fail_silently=False,
            )

            messages.success(request, '認証コードを送信しました。メールをご確認ください。')
            return redirect('verify_email')
        else:
            messages.error(request, '入力内容に誤りがあります。')

    return render(request, '1_user/新規登録/register.html')

# 認証コードの検証
def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        session_code = request.session.get('verification_code')
        email = request.session.get('email')

        if int(code) != session_code:
            messages.error(request, '認証コードが間違っています。')
            return redirect('verify_email')

        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create_user(email=email, password='temporary_password')
            user.save()

        messages.success(request, '認証が成功しました。新しいパスワードを設定してください。')
        return redirect('reset_password')

    return render(request, '1_user/新規登録/verify_email.html')

# パスワードリセット
def password_reset_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, '登録されていないメールアドレスです。')
            return redirect('password_reset_email')

        verification_code = random.randint(1000, 9999)
        request.session['verification_code'] = verification_code
        request.session['email'] = email

        send_mail(
            'パスワードリセット認証コード',
            f'以下の認証コードを入力してください: {verification_code}',
            'info001@meltfire.net',
            [email],
            fail_silently=False,
        )

        messages.success(request, '認証コードを送信しました。メールをご確認ください。')
        return redirect('verify_email')

    return render(request, '1_user/ログイン_ログアウト/password_reset_email.html')

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('email')

        if new_password != confirm_password:
            messages.error(request, 'パスワードが一致しません。')
            return redirect('reset_password')

        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        messages.success(request, 'パスワードが更新されました。ログインしてください。')
        return redirect('login')

    return render(request, '1_user/ログイン_ログアウト/reset_password.html')

# ログイン処理
def login_view(request):
    remove_duplicate_messages(request)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'ログインに成功しました！')
                return redirect('home')
            else:
                messages.error(request, 'メールアドレスまたはパスワードが正しくありません。')
        except User.DoesNotExist:
            messages.error(request, 'このメールアドレスは登録されていません。')

    return render(request, '1_user/ログイン_ログアウト/login.html')

# ログアウト処理
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('home')

# マイページ
def mypage(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.self_intro = request.POST.get('self_intro', '')
        profile.current_position = request.POST.get('current_position', '')
        profile.qualifications = request.POST.get('qualifications', '')
        profile.target_qualifications = request.POST.get('target_qualifications', '')
        profile.save()
        messages.success(request, 'プロフィールが保存されました！')
        return redirect('mypage')

    return render(request, '1_user/プロフィール/mypage.html', {'profile': profile})

# 自己分析画面
def self_analysis(request):
    return render(request, '1_user/自己分析/self_analysis.html')

# 分析結果画面
def result_analysis(request):
    return render(request, '1_user/自己分析/result_analysis.html')

# --- コミュニティ関連ビュー ---

# スレッド一覧表示
def community_thread(request):
    threads = Thread.objects.all().prefetch_related('comments').order_by('-updated_at')
    return render(request, '1_user/コミュフォ/community_thread.html', {'threads': threads})
    threads = Thread.objects.prefetch_related('comments').all()
    return render(request, 'community_thread.html', {'threads': threads})

# スレッド作成
def create_thread(request):
    if request.method == 'POST':
        category_key = request.POST.get('category')
        content = request.POST.get('content')

        if not category_key or not content:
            return render(request, '1_user/コミュフォ/community_thread.html', {'error': 'カテゴリと内容は必須です'})

        category_dict = dict(Thread.CATEGORY_CHOICES)
        category = category_dict.get(category_key, category_key)

        thread = Thread.objects.create(
            category=category,
            created_by=request.user
        )

        Comment.objects.create(
            content=content,
            thread=thread,
            author=request.user
        )

        return redirect(reverse('comment', kwargs={'thread_id': thread.id}))

    return render(request, '1_user/コミュフォ/community_thread.html')

# スレッド詳細表示
def comment(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    category_display = dict(Thread.CATEGORY_CHOICES).get(thread.category, thread.category)
    comments = thread.comments.all().order_by('created_at')
    first_comment = comments.first() if comments.exists() else None
    other_comments = comments[1:] if comments.count() > 1 else []

    return render(request, '1_user/コミュフォ/comment.html', {
        'thread': thread,
        'category_display': category_display,
        'first_comment': first_comment,
        'comments': other_comments
    })

# コメント投稿
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Thread, Comment

def post_comment(request, thread_id):
    if request.method == 'POST':
        thread = get_object_or_404(Thread, id=thread_id)
        content = request.POST.get('comment')

        if content:
            Comment.objects.create(
                thread=thread,
                author=request.user,
                content=content,
            )
        else:
            messages.error(request, 'コメント内容を入力してください。')

        return redirect('comment', thread_id=thread.id)


# --- 管理者関連ビュー ---

# 管理者ダッシュボード
def admin_dashboard(request):
    return render(request, '2_admin/1_ホームログイン/admindashboard.html')

# 管理者ログイン
def admin_login(request):
    return render(request, '2_admin/1_ホームログイン/adminlogin.html')

# ユーザーリスト管理
def user_list(request):
    return render(request, '2_admin/ユーザー管理/user_list.html')

# スレッド詳細（管理者用）
def thread_view(request):
    return render(request, '2_admin/コミュフォ/thread_view.html')

# プロフィール保存処理
def save_profile(request):
    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.self_intro = request.POST.get('self_intro', '')
        profile.current_position = request.POST.get('current_position', '')
        profile.qualifications = request.POST.get('qualifications', '')
        profile.target_qualifications = request.POST.get('target_qualifications', '')
        profile.save()
        messages.success(request, 'プロフィールが保存されました。')
    return redirect('mypage')

# スレッド報告処理
def report_thread(request, thread_id):
    if request.method == 'POST':
        try:
            thread = Thread.objects.get(id=thread_id)
            thread.report_count += 1
            thread.save()
            return JsonResponse({'success': True, 'message': 'スレッドが報告されました。'})
        except Thread.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'スレッドが見つかりませんでした。'}, status=404)
    return JsonResponse({'success': False, 'error': '無効なリクエストです。'}, status=400)

# コメント報告処理
def report_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.is_reported = True
            comment.save()
            return JsonResponse({'success': True, 'message': 'コメントが報告されました。'})
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'コメントが見つかりませんでした。'}, status=404)
    return JsonResponse({'success': False, 'error': '無効なリクエストです。'}, status=400)

# カテゴリ別スレッド取得
def get_threads_by_category(request):
    category = request.GET.get('category', None)
    category_map = dict(Thread.CATEGORY_CHOICES)
    category_jp = category_map.get(category)

    if category and not category_jp:
        return JsonResponse({'error': '無効なカテゴリです'}, status=400)

    threads = Thread.objects.filter(category=category_jp).order_by('-updated_at') if category_jp else Thread.objects.all().order_by('-updated_at')

    thread_list = [{
        'id': thread.id,
        'category': thread.category,
        'created_by': thread.created_by.username,
        'first_comment': thread.comments.first().content if thread.comments.exists() else 'コメントがありません',
        'last_updated': thread.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'comment_count': thread.comments.count(),
    } for thread in threads]

    return JsonResponse({'threads': thread_list})


# レポートアイテム
def report_item(request, model, report_field, **kwargs):
    item_id = kwargs.get('comment_id') or kwargs.get('thread_id')
    print(f"[DEBUG] Request Method: {request.method}, Item ID: {item_id}, Model: {model}, Report Field: {report_field}")

    if request.method == 'POST':
        try:
            item = get_object_or_404(model, id=item_id)
            user_report_data, _ = UserReportData.objects.get_or_create(user=request.user)

            if getattr(user_report_data, f"has_reported_{report_field}")(item_id):
                print(f"[DEBUG] {report_field.capitalize()} ID {item_id} already reported by User {request.user.id}")
                return JsonResponse({'error': f'この{report_field}は既に報告されています。'}, status=400)

            getattr(user_report_data, f"add_reported_{report_field}")(item_id)
            item.report_count += 1
            item.reported_by_users.add(request.user)
            item.save()
            print(f"[DEBUG] Report Successful: {report_field.capitalize()} ID {item_id}, User ID {request.user.id}")
            return JsonResponse({'success': f'{report_field}を報告しました。'})

        except Exception as e:
            print(f"[ERROR] Exception in Reporting {report_field.capitalize()} ID {item_id}: {e}")
            return JsonResponse({'error': '内部エラーが発生しました。'}, status=500)

    print(f"[DEBUG] Invalid Request Method {request.method} for {report_field.capitalize()} ID {item_id}")
    return JsonResponse({'error': '無効なリクエストです。'}, status=400)



from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment, UserReportData

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = thread.comments.all()

    # スレッドが報告済みか確認
    is_thread_reported = UserReportData.objects.filter(
        user=request.user,
        reported_threads_list__contains=str(thread_id)
    ).exists()

    # 各コメントが報告済みか確認
    for comment in comments:
        comment.is_reported_by_user = UserReportData.objects.filter(
            user=request.user,
            reported_comments_list__contains=str(comment.id)
        ).exists()

    return render(request, '1_user/コミュフォ/thread_detail.html', {
        'thread': thread,
        'is_thread_reported': is_thread_reported,
        'comments': comments,
    })


# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_user_report_data(request):
    user = request.user
    user_report_data, _ = UserReportData.objects.get_or_create(user=user)
    return JsonResponse({
        'reported_threads': user_report_data.get_reported_threads_list(),
        'reported_comments': user_report_data.get_reported_comments_list(),
    })


























#-------------------------------------------------------------------------管理者サイド--------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
import os
from decouple import config
# 管理者の固定IDとパスワード
ADMIN_CREDENTIALS = {
    "admin_id": "nikakih",
    "password": "kazuma0129"
}



ALLOWED_IPS = ['127.0.0.1', '192.168.0.1']

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def admin_login(request):
    client_ip = get_client_ip(request)
    if client_ip not in ALLOWED_IPS:
        return HttpResponseForbidden("アクセスが許可されていません。")

    if request.method == "POST":
        admin_id = request.POST.get("admin_id")
        password = request.POST.get("password")

        if admin_id == ADMIN_CREDENTIALS["admin_id"] and password == ADMIN_CREDENTIALS["password"]:
            request.session['is_admin'] = True
            return redirect('admin_dashboard')

        error_message = "IDまたはパスワードが間違っています。"
        return render(request, '2_admin/admin_login.html', {"error_message": error_message})

    return render(request, '2_admin/admin_login.html')

def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    return render(request, '2_admin/admin_dashboard.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


from django.shortcuts import render
from .models import Thread

def admin_community_thread(request):
    threads = Thread.objects.all()  # すべてのスレッドを取得
    return render(request, '2_admin/admin_community_thread.html', {'threads': threads})



from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment

def admin_comment(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = thread.comments.all()
    return render(request, '2_admin/admin_comment.html', {'thread': thread, 'comments': comments})


from django.shortcuts import render

def admin_user_list(request):
    # 仮のユーザーリストデータ
    users = [
        {'id': 1, 'name': 'ユーザー1', 'email': 'user1@example.com'},
        {'id': 2, 'name': 'ユーザー2', 'email': 'user2@example.com'},
    ]
    return render(request, '2_admin/admin_user_list.html', {'users': users})

from django.shortcuts import render
from .models import Thread, Comment

def admin_report_list(request):
    # 報告されたスレッドとコメントを取得
    reported_threads = Thread.objects.filter(report_count__gt=0)
    reported_comments = Comment.objects.filter(report_count__gt=0)

    context = {
        'reported_threads': reported_threads,
        'reported_comments': reported_comments,
    }
    return render(request, '2_admin/admin_report_list.html', context)


from django.http import JsonResponse
from .models import Comment

def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return JsonResponse({'status': 'success'})
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'コメントが見つかりませんでした。'})
    return JsonResponse({'status': 'error', 'message': '無効なリクエストです。'})
from django.db.models import Count, Q


def get_admin_threads(request):
    sort_by = request.GET.get('sort_by', 'thread_reports')

    if sort_by == 'comment_reports':
        threads = Thread.objects.annotate(
            reported_comment_count=Count('comments', filter=Q(comments__is_reported=True))
        ).order_by('-reported_comment_count')
    else:
        threads = Thread.objects.order_by('-report_count')

    thread_list = []
    for thread in threads:
        first_comment = thread.comments.first()  # 最初のコメントを取得
        print(f"[DEBUG] Thread ID: {thread.id}, First Comment: {first_comment}")  # デバッグ出力
        thread_list.append({
            'id': thread.id,
            'created_by': thread.created_by.username,
            'first_comment': first_comment.content if first_comment else 'コメントなし',
            'updated_at': thread.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'report_count': thread.report_count,
            'reported_comment_count': thread.comments.filter(is_reported=True).count(),
        })

    # ここでデバッグ出力
    from pprint import pprint
    pprint(thread_list)

    return JsonResponse({'threads': thread_list})


from django.http import JsonResponse

def get_threads_sorted_by_report_count(request):
    threads = Thread.objects.all().order_by('-report_count')
    thread_list = [{
        'id': thread.id,
        'created_by': thread.created_by.username,
        'first_comment': thread.comments.first().content if thread.comments.exists() else 'コメントがありません',
        'last_updated': thread.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'report_count': thread.report_count,
        'reported_comment_count': thread.comments.filter(is_reported=True).count(),
    } for thread in threads]

    return JsonResponse({'threads': thread_list})


def get_threads_sorted_by_comment_report_count(request):
    threads = Thread.objects.all()
    threads = sorted(
        threads,
        key=lambda t: t.comments.filter(is_reported=True).count(),
        reverse=True
    )
    thread_list = [{
        'id': thread.id,
        'created_by': thread.created_by.username,
        'first_comment': thread.comments.first().content if thread.comments.exists() else 'コメントがありません',
        'last_updated': thread.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'report_count': thread.report_count,
        'reported_comment_count': thread.comments.filter(is_reported=True).count(),
    } for thread in threads]

    return JsonResponse({'threads': thread_list})





