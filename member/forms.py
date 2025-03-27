from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm

from utils.forms import BootstrapModelForm

# 유저 모델 가져오기
# get_user_model()을 하면 settings에 설정된 AUTH_USER_MODEL 을 가져옴
# Auth유저를 바꿨기 때문에
User = get_user_model()

# UserCreationForm을 상속하여, 이메일과 닉네임 기반 회원가입 폼을 커스터마이징한 것.
class SignupForm(UserCreationForm):

    # 폼 필드의 속성을 수정
    # User 모델에 존재하지않지만 폼에서 필요한 필드를 추가하기 위해 사용
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

    # User 모델을 사용해 폼에 포함시킬 필드 및 속성 설정
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

# 로그인 폼을 정의함. 사용자 인증을 위해 사용.
class LoginForm(forms.Form):
    email = forms.CharField(
        label = '이메일',
        required = True,
        widget = forms.EmailInput(
            attrs = {
                    'placeholder' : 'example@example.com',
                    'class' : 'form-control',
            }
        )
    )
    password = forms.CharField(
        label="패스워드",
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                    'placeholder' : 'password',
                    'class' : 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    # 전체 폼의 유효성 검사를 담당.
    # is_valid할 때 clean매서드가 호출됨
    def clean(self):
        cleaned_data = super().clean() # is_valid 후 clean한 데이터가 들어옴.
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # authenticate 이메일(또는 사용자 이름)과 비밀번호로 인증하기 위해 사용하는 함수
        # 인증 후 유저 객체 또는 None 반환
        self.user = authenticate(email=email, password=password)
        # user = authenticate(email=email, password=password)

        if not self.user:
            raise forms.ValidationError('이메일 또는 패스워드가 올바르지 않습니다.')

        if not self.user.is_active:
            raise forms.ValidationError('유저가 인증되지 않았습니다.')

        return cleaned_data
        # return cleaned_data.get('email')

class NicknameForm(BootstrapModelForm):
    class Meta:
        model = User
        fields = ('nickname',)
        labels = {
            'nickname':'닉네임을 입력하여 회원가입을 마무리해주세요.'
        }