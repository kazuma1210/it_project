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
