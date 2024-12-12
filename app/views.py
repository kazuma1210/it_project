from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import random
import string
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

EMAIL_HOST_PASSWORD = os.getenv('MAILTRAP_PASSWORD', '')

def register(request):
    return render(request, '1_user/新規登録/register.html')
 # 適切なテンプレートを返す


# ホーム画面
def home(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'ゲスト',
    }
    return render(request, '1_user/ホーム/home.html', context)


# メール認証用コードの生成
def generate_verification_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# メール送信関数（認証コード）
def send_verification_email(email, code):
    subject = 'アカウントの認証コード'
    message = f'以下の認証コードを入力してください:\n\n{code}'
    from_email = 'your_email@example.com'  # 設定したメールアドレス
    send_mail(subject, message, from_email, [email])



# メール認証画面
def verify_email(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        session_code = request.session.get('verification_code')

        if entered_code == session_code:
            # コードが一致した場合、ユーザーをアクティブにする
            user = request.user
            user.is_active = True  # ユーザーをアクティブにする
            user.save()
            messages.success(request, 'アカウントが有効化されました！')
            return redirect('home')  # home.htmlにリダイレクト
        else:
            messages.error(request, '認証コードが間違っています。')
            return render(request, '1_user/新規登録/verify_email.html')

    return render(request, '1_user/新規登録/verify_email.html')


# ログアウト処理
def user_logout(request):
    logout(request)  # ユーザーをログアウト
    return redirect('home')  # ログアウト後、ホームページへリダイレクト


# アカウント有効化（トークンによる）
def send_activation_email(user):
    token = default_token_generator.make_token(user)  # トークン生成
    uid = urlsafe_base64_encode(str(user.pk).encode())  # ユーザーIDエンコード
    activation_link = f'http://yourdomain.com/activate/{uid}/{token}/'  # URLリンク生成

    subject = 'アカウントの有効化'
    body = f'以下のリンクをクリックしてアカウントを有効化してください。\n\n{activation_link}'

    send_mail(subject, body, 'from_email@example.com', [user.email])  # メール送信


# アカウント有効化用のビュー（トークン検証）
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # ユーザーIDをデコード
        user = get_user_model().objects.get(pk=uid)  # ユーザーを取得
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None  # ユーザーが見つからなかった場合

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # ユーザーを有効化
        user.save()
        login(request, user)  # ユーザーをログインさせる
        return redirect('home')  # 任意のリダイレクト先（ホームページなど）
    else:
        return render(request, 'account/activation_invalid.html')  # トークンが無効な場合


# 各ページビュー
def self_analysis(request):
    return render(request, '1_user/自己分析/self_analysis.html')


def result_analysis(request):
    return render(request, '1_user/自己分析/result_analysis.html')


def community_thread(request):
    return render(request, '1_user/コミュフォ/community_thread.html')


def mypage(request):
    return render(request, '1_user/プロフィール/mypage.html')


def signup(request):
    context = {}
    return render(request, '1_user/新規登録/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # ユーザーを認証する
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # ユーザーが存在すればログイン
                login(request, user)
                return redirect('home')  # ログイン後のリダイレクト先を指定
            else:
                # ユーザーが認証されなかった場合のエラーメッセージ
                form.add_error(None, "メールアドレスまたはパスワードが正しくありません。")
    else:
        form = LoginForm()
    return render(request, '1_user/ログイン_ログアウト/login.html', {'form': form})

def logout_confirm(request):
    context = {}
    return render(request, '1_user/ログイン_ログアウト/logout_confirm.html', context)


def logout(request):
    context = {}
    return render(request, '1_user/ログイン_ログアウト/logout.html', context)


def community_thread(request):
    context = {}
    return render(request, '1_user/コミュフォ/community_thread.html', context)


def admin_dashboard(request):
    context = {}
    return render(request, '2_admin/1_ホームログイン/admindashboard.html', context)


def admin_login(request):
    context = {}
    return render(request, '2_admin/1_ホームログイン/adminlogin.html', context)


def user_list(request):
    context = {}
    return render(request, '2_admin/ユーザー管理/user_list.html', context)


def thread_view(request):
    context = {}
    return render(request, '2_admin/コミュフォ/thread_view.html', context)
