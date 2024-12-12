from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(widget=forms.PasswordInput(), label='パスワード')
    # その他必要なフィールドを追加
