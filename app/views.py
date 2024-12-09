from django.shortcuts import render



def home(request):
    return render(request, 'home.html')  # ホーム画面
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'ゲスト',
    }
    return render(request, 'home.html', context)


def self_analysis(request):
    return render(request, 'self_analysis.html')  # app/ は不要

def mypage(request):
    return render(request, 'mypage.html')  # ユーザー情報画面

def community_thread(request):
    return render(request, 'community_thread.html')  # communitythread

def result_analysis(request):
    return render(request, 'result_analysis.html')  # result_analysis