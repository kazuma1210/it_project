from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'メールアドレスを入力',
            'id': 'email'
        }),
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワードを入力',
            'id': 'password'
        }),
    )
