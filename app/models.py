from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

# カスタムユーザーモデル
CATEGORY_CHOICES = [
    ('national', '国家資格'),
    ('vendor', 'ベンダー資格'),
    ('programming', 'プログラミング言語'),
    ('software', 'ソフトウェア'),
    ('hardware', 'ハードウェア'),
    ('database', 'データベース'),
    ('network', 'ネットワーク'),
    ('security', 'セキュリティ'),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=191)  # 制限を191に変更

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # 他と競合しないよう設定
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # 他と競合しないよう設定
        blank=True,
    )

# プロフィールモデル
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # カスタムユーザーモデルを参照
        on_delete=models.CASCADE
    )
    self_intro = models.TextField(blank=True, null=True)
    current_position = models.CharField(max_length=191, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    target_qualifications = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

# スレッドモデル
from django.db import models
from django.conf import settings


import uuid

from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Thread(models.Model):
    CATEGORY_CHOICES = [
        ('national', '国家資格'),
        ('vendor', 'ベンダー資格'),
        ('programming', 'プログラミング言語'),
        ('software', 'ソフトウェア'),
        ('hardware', 'ハードウェア'),
        ('database', 'データベース'),
        ('network', 'ネットワーク'),
        ('security', 'セキュリティ'),
    ]
    id = models.AutoField(primary_key=True)  # デフォルトの主キーをそのまま使用
    thread_id = models.CharField(max_length=50, unique=True, null=True, blank=True)  # ユニークなスレッドID
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.thread_id:  # 新規作成時のみ生成
            self.thread_id = f"thread-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)





class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    report_count = models.IntegerField(default=0)
