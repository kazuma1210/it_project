from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, Thread, Comment
from .forms import CustomUserCreationForm, CommentForm
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Thread
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Thread
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
from .models import Thread, Comment
User = get_user_model()  # カスタムユーザーモデルを使用

# パスワードをリセットする例
def reset_password_example():
    try:
        user = User.objects.get(email='craft20041210@gmail.com')
        user.set_password('kazuma0129')  # パスワードを設定
        user.save()
        print("パスワードが正しくリセットされました。")
    except User.DoesNotExist:
        print("指定されたユーザーは存在しません。")

# ホーム画面
def home(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'ゲスト',
    }
    return render(request, '1_user/ホーム/home.html', context)

# 新規登録処理
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # 新規登録したユーザーをデータベースに保存
            messages.success(request, 'アカウントが作成されました！ログインしてください。')
            return redirect('login')  # ログインページへリダイレクト
        else:
            messages.error(request, '入力内容に誤りがあります。もう一度お試しください。')
    else:
        form = CustomUserCreationForm()

    return render(request, '1_user/新規登録/register.html', {'form': form})

# ログイン処理
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
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
        else:
            messages.error(request, 'メールアドレスを入力してください。')
    return render(request, '1_user/ログイン_ログアウト/login.html')

# ログアウト処理
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('home')

# マイページ（プロフィールの保存）
@login_required
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

# コミュニティスレッド一覧表示
@login_required
def community_thread(request):
    threads = Thread.objects.all().prefetch_related('comments').order_by('-updated_at')
    return render(request, '1_user/コミュフォ/community_thread.html', {'threads': threads})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Comment
from django.urls import reverse

# スレッド作成処理
def create_thread(request):
    if request.method == 'POST':
        category_key = request.POST.get('category')  # 英語のキーを取得
        content = request.POST.get('content')

        # カテゴリと内容が必須
        if not category_key or not content:
            return render(request, '1_user/コミュフォ/community_thread.html', {'error': 'カテゴリと内容は必須です'})

        # スレッドを作成
        thread = Thread.objects.create(
            category=dict(Thread.CATEGORY_CHOICES).get(category_key, category_key),  # 日本語に変換
            created_by=request.user
        )

        # スレッドの初コメントを作成
        Comment.objects.create(
            category=dict(Thread.CATEGORY_CHOICES).get(category_key, category_key),  # 日本語に変換
            content=content,
            thread=thread,
            author=request.user
        )

        # スレッド詳細ページにリダイレクト
        return redirect(reverse('comment', kwargs={'thread_id': thread.id}))

    return render(request, '1_user/コミュフォ/community_thread.html')


# スレッド詳細（コメント一覧表示）
@login_required








def comment(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    # CATEGORY_CHOICESから日本語ラベルを取得
    category_display = dict(Thread.CATEGORY_CHOICES).get(thread.category, thread.category)

    comments = thread.comments.all().order_by('created_at')
    first_comment = comments.first() if comments.exists() else None
    other_comments = comments[1:] if comments.count() > 1 else []

    return render(request, '1_user/コミュフォ/comment.html', {
        'thread': thread,
        'category_display': category_display,  # 日本語ラベルを渡す
        'first_comment': first_comment,
        'comments': other_comments
    })



# コメント投稿
@login_required
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

# 管理者用ダッシュボード
@login_required
def admin_dashboard(request):
    return render(request, '2_admin/1_ホームログイン/admindashboard.html')

# 管理者ログイン
def admin_login(request):
    return render(request, '2_admin/1_ホームログイン/adminlogin.html')

# ユーザーリスト管理
@login_required
def user_list(request):
    return render(request, '2_admin/ユーザー管理/user_list.html')

# スレッドの詳細画面（管理者用）
@login_required
def thread_view(request):
    return render(request, '2_admin/コミュフォ/thread_view.html')

# プロフィール保存処理（個別関数）
@login_required
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


@csrf_exempt


@csrf_exempt
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

from .models import Comment

@csrf_exempt
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

