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

def community_forum(request):
    return render(request, 'community_forum.html')  # コミュニティフォーラム画面

def user_info(request):
    return render(request, 'user_info.html')  # ユーザー情報画面
