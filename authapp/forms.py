from django.contrib.auth.forms import AuthenticationForm, forms, UserCreationForm, UserChangeForm
from authapp.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control textinput textInput'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control textinput textInput'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'age', 'avatar', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Логин',
                'class': 'textinput textInput form-control'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Пароль',
                'class': 'textinput textInput form-control'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Подтвердите пароль',
                'class': 'textinput textInput form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Имя',
                'class': 'textinput textInput form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Фамилия',
                'class': 'textinput textInput form-control'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Возраст',
                'class': 'textinput textInput form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'placeholder': 'Аватар',
                'class': 'textinput textInput form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Почта',
                'class': 'textinput textInput form-control'
            })
        }


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'age', 'avatar', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Логин',
                'class': 'textinput textInput form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Имя',
                'class': 'textinput textInput form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Фамилия',
                'class': 'textinput textInput form-control'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Возраст',
                'class': 'textinput textInput form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'placeholder': 'Аватар',
                'class': 'textinput textInput form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Почта',
                'class': 'textinput textInput form-control'
            })
        }