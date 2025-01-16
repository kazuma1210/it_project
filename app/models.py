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

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=191)  # 必須フィールド
    username = models.CharField(max_length=150, unique=True)  # 必須フィールドとして復活

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

    USERNAME_FIELD = 'email'  # ログインに使用するフィールドを email に設定
    REQUIRED_FIELDS = ['username']  # アカウント作成時に username を必須に

    objects = BaseUserManager()

    def __str__(self):
        return self.username



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # username を含める



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
import json
import uuid


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
    id = models.AutoField(primary_key=True)
    thread_id = models.CharField(max_length=50, unique=True, null=True, blank=True)  # ユニークなスレッドID
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    report_count = models.IntegerField(default=0)  # 報告数を記録
    reported_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reported_threads', blank=True)

    def save(self, *args, **kwargs):
        if not self.thread_id:  # 新規作成時のみ生成
            self.thread_id = f"thread-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)


class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    category = models.CharField(max_length=50, choices=Thread.CATEGORY_CHOICES)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    report_count = models.IntegerField(default=0)  # 報告数を記録
    reported_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reported_comments', blank=True)


from django.db import models
from django.conf import settings

class UserReportData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reported_threads = models.IntegerField(default=0)
    reported_comments = models.IntegerField(default=0)
    reported_threads_list = models.TextField(default="[]", null=True, blank=True)
    reported_comments_list = models.TextField(default="[]", null=True, blank=True)

    def get_reported_threads_list(self):
        if not self.reported_threads_list:
            return []
        return json.loads(self.reported_threads_list)

    def add_reported_thread(self, thread_id):
        threads = self.get_reported_threads_list()
        if thread_id not in threads:
            threads.append(thread_id)
            self.reported_threads_list = json.dumps(threads)
            self.reported_threads += 1
            self.save()

    def has_reported_thread(self, thread_id):
        return thread_id in self.get_reported_threads_list()

    def get_reported_comments_list(self):
        if not self.reported_comments_list:
            return []
        return json.loads(self.reported_comments_list)

    def add_reported_comment(self, comment_id):
        comments = self.get_reported_comments_list()
        if comment_id not in comments:
            comments.append(comment_id)
            self.reported_comments_list = json.dumps(comments)
            self.reported_comments += 1
            self.save()

    def has_reported_comment(self, comment_id):
        return comment_id in self.get_reported_comments_list()

