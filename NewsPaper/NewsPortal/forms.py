from django import forms
from .models import Post
from django.contrib.auth.models import User


class CreatePost(forms.ModelForm):
    category = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    content = forms.Textarea()

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
                    ]
        widgets = {
            'content': forms.Textarea(attrs={'cols': 120, 'rows': 10}),
        }


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


