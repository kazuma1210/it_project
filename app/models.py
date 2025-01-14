from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth.models import BaseUserManager  # 必要なインポートを追加

    # 実装


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
    email = models.EmailField(unique=True, max_length=191)
    username = None  # `username` フィールドを削除

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
    )

    USERNAME_FIELD = 'email'  # ログインに使用するフィールドを `email` に設定
    REQUIRED_FIELDS = []  # 必須フィールドに `email` のみ設定


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


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

class UserReportData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reported_threads = models.IntegerField(default=0)
    reported_comments = models.IntegerField(default=0)


