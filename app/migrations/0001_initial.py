# Generated by Django 3.1.14 on 2025-01-16 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReportData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reported_threads_list', models.TextField(blank=True, default='[]', null=True)),
                ('reported_comments_list', models.TextField(blank=True, default='[]', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('thread_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('category', models.CharField(choices=[('national', '国家資格'), ('vendor', 'ベンダー資格'), ('programming', 'プログラミング言語'), ('software', 'ソフトウェア'), ('hardware', 'ハードウェア'), ('database', 'データベース'), ('network', 'ネットワーク'), ('security', 'セキュリティ')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('report_count', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reported_by_users', models.ManyToManyField(blank=True, related_name='reported_threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self_intro', models.TextField(blank=True, null=True)),
                ('current_position', models.CharField(blank=True, max_length=191, null=True)),
                ('qualifications', models.TextField(blank=True, null=True)),
                ('target_qualifications', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=191, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_groups', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('national', '国家資格'), ('vendor', 'ベンダー資格'), ('programming', 'プログラミング言語'), ('software', 'ソフトウェア'), ('hardware', 'ハードウェア'), ('database', 'データベース'), ('network', 'ネットワーク'), ('security', 'セキュリティ')], max_length=50)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('report_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reported_by_users', models.ManyToManyField(blank=True, related_name='reported_comments', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.thread')),
            ],
        ),
    ]
