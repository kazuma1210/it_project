from django.contrib import admin
from .models import Thread, Comment

# デコレーター形式でモデルを登録
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'created_by', 'created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'author', 'created_at', 'report_count')

