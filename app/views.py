from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.core.mail import send_mail
import random
import string
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



# ホーム画面
def home(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'ゲスト',
    }
    return render(request, 'home.html', context)


# メール認証用コードの生成
def generate_verification_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# メール送信関数（認証コード）
def send_verification_email(email, code):
    subject = 'アカウントの認証コード'
    message = f'以下の認証コードを入力してください:\n\n{code}'
    from_email = 'your_email@example.com'  # 設定したメールアドレス
    send_mail(subject, message, from_email, [email])


# ユーザー登録ビュー
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ユーザー登録
            email = user.email  # 登録したユーザーのメールアドレス

            # メール認証に必要な情報を設定
            verification_code = generate_verification_code()  # 認証コード生成
            send_verification_email(email, verification_code)  # メール送信

            # 認証コードをセッションに保存（後で確認）
            request.session['verification_code'] = verification_code

            # ユーザーに認証コード入力画面にリダイレクト
            return redirect('verify_email')  # メール認証画面へリダイレクト
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


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
            return render(request, 'verify_email.html')

    return render(request, 'verify_email.html')


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


# 自己分析ページ
def self_analysis(request):
    return render(request, 'self_analysis.html')    


# 結果分析ページ
def result_analysis(request):
    return render(request, 'result_analysis.html')


# コミュニティフォーラムページ
def community_thread(request):
    return render(request, 'community_thread.html')  


# マイページビュー
def mypage(request):
    return render(request, 'mypage.html')  # mypage.htmlをレンダリング
