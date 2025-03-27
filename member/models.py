from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from utils.models import TimestampModel


# 사용자 지정 메니져
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요.')
        user = self.model (
            email = self.normalize_email(email),
        )
        user.set_password(password) # 해시화
        user.is_active = False
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        from django.utils.crypto import get_random_string
        return get_random_string(length, allowed_chars)

# 암호화는 복호화가 가능함
# 암호화는 qwer1234 -> aslkfjdslkfj322kj43 -> 복호화 -> qwer1234
# 해시화는 복호화가 불가능함
# 해시화 qwer1234 -> aslkfjdslkfj322kj43 -> 일부분 암호화(aslkfj) -> 암호화를 반복 -> sldkfjsdlf -> 소실된 부분 때문에 복호화가 불가능
# 장고는 SHA256를 사용
# SHA-256은 암호학에서 사용하는 해시 함수(hash function) 중 하나예요. 주로 데이터 무결성 확인, 비밀번호 저장, 디지털 서명, 블록체인 같은 곳에 쓰임.

class User(AbstractBaseUser):  # 기본 기능은 상속받아서 사용
    email = models.EmailField(
        verbose_name='email',
        unique = True
    )
    is_active = models.BooleanField(default = False) # 기본적으로 비활성화 시켜놓고 확인 후 활성화
    is_admin = models.BooleanField(default = False)  # admin 기능
    # is_staff = models.BooleanField(default = False)  # is_staff 기능
    # is_superuser = models.BooleanField(default = False)  # is_superuser 기능
    nickname = models.CharField('nickname', max_length=20, unique=True)
    # 나를 팔로우 하는 사람이 팔로워
    # 내가 팔로우 하는 사람이 팔로잉
    # User N:N User
    # a <=> b symmetrical = True
    # a => b symmetrical = False
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers',
        through='UserFollowing', through_fields=('from_user', 'to_user')
    )  # 'self' User가 User를 받을 수 없어서 self사용

    # 사용자 지정 메니져
    # User.objects.all()   <- objects가 메니져
    objects = UserManager()  # 메니져는 UserManager()
    USERNAME_FIELD = 'email'  # 기본 유저네임(아이디)를 email로 지정
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_full_name(self): # 사용자의 전체 이름(Full name)을 반환. 성과 이름을 합침
        # return f"{self.first_name} {self.last_name}"
        return self.nickname

    def get_short_name(self):  # 일반적으로 닉네임, 이름(first name) 등을 반환
        return self.nickname

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

# @property
# 함수는 user.is_superuser() 이렇게 쓰는걸 user.c 이렇게 변수처럼 쓸 수 있게 만들어줌
# 기존에 존재하는 컬럼 is_superuser, is_superuser가 가진 기능을 사용하려고 사용.
# 혹은  is_superuser = models.BooleanField(default = False) 이렇게 필드를 만들어 줘도 되지만 해당 필드를 사용하지 않을거기 때문에 @property사용

# AbstractBaseUser: Django의 추상 기반 클래스 중 하나로, 비밀번호 및 인증 관련 필드와 메서드만을 제공하며, 사용자 정의 필드를 추가하여 완전한 User 모델을 구성할 수 있습니다.

# superuser 생성
# python manage.py createsuperuser
# 커스텀 유저 모델에 유저 이름과 이메일을 모두 이메일로 지정했기 때문에 유저 이름을 묻지 않고 이메일만 물어봄

class UserFollowing(TimestampModel):
    # 팔로워
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followers')
    # 팔로잉
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')

    class Meta:
        # 두 값을 합쳐서 unique
        unique_together = ('to_user', 'from_user')
        # to_user 1, from_user 2
        # to_user 1, from_user 3
        # to_user 1, from_user 2 => 오류'
