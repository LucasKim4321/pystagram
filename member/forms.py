from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# 유저 모델 가져오기
# get_user_model()을 하면 settings에 설정된 AUTH_USER_MODEL 을 가져옴
# Auth유저를 바꿨기 때문에
User = get_user_model()

class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # class_default_fields = ('password1', 'password2')
        # for field in class_default_fields:
        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = 'password'
            if field.startswith('password1'):
                self.fields[field].label = '비밀번호'
            else:
                self.fields[field].label = '비밀번호 확인'


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'nickname',)
        labels = {
            'email' : '이메일',
            'nickname': '닉네임',
        }
        widgets = {
            'email' : forms.EmailInput(
                attrs= {
                    'placeholder' : 'example@example.com',
                    'class' : 'form-control',
                }
            ),
            'nickname': forms.TextInput(
                attrs= {
                    'placeholder':'닉네임',
                    'class': 'form-control',
                }
            )
        }