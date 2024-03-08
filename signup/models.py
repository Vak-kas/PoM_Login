from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime

# Create your models here.

class UserManager(BaseUserManager):
    #새로운 사용자를 생성하고 데이터베이스에 저장하는 기능 수행
    def create_user(self, email, password=None, **extra_fields): #이메일, 비밀번호, 그외 추가 필드 인자
        if not email: #이메일이 제공되지 않으면 오류 처리
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email) #이메일 정규화.
        user = self.model(email=email, **extra_fields) #사용자 인스턴스 생성. UserManager 가 연결된 사용자 모델 참조
        user.set_password(password) #사용자 비밀번호 설정
        user.save(using=self._db) #비밀번호를 해시하여 저장, 평문 비밀번호가 데이터베이스에 직접 저장 X
        return user

    # 관리자 권한을 가진 사용자 생성하는 기능
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # 필수 필드에 대한 기본값 설정
        extra_fields.setdefault('birthdate', '1990-01-01')
        extra_fields.setdefault('name', 'Admin')
        extra_fields.setdefault('nickname', 'admin')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True) #인덱스
    email = models.EmailField(unique=True) #이메일, 아이디로 사용
    name = models.CharField(max_length=50) #이름
    phone = models.CharField(max_length=15) #핸드폰 번호
    birthdate = models.DateField() #생년월일
    addr = models.CharField(max_length=50) #주소
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')]) #성별
    user_type = models.CharField(max_length=10, choices=[('e', 'Enterprise'), ('i', 'Individual'), ('a', "Admin")]) #유저 등급
    nickname = models.CharField(max_length=8, unique=True) #닉네임, 별명
    password = models.CharField(max_length=100)  # 비밀번호

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname']  # createsuperuser 관리 명령 사용할 때 추가로 입력 요구하는 필드

    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.email  # 필요에 따라 'self.name' 또는 'self.nickname'으로 변경 가능

class Enterprise(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100) #회사명
    company_code = models.CharField(max_length = 100, unique=True, null = True, blank=True) #회사 코드
    department = models.CharField(max_length=100) #부서
    position = models.CharField(max_length=100) #직책

    def __str__(self):
        return self.company_name

class Individual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, null=True, blank=True)  # 학교, 비어있어도 됨
    department = models.CharField(max_length=100, null=True, blank=True)  # 학과, 비어있어도 됨

    def __str__(self):
        return self.user.name




class TempEmailVerify(models.Model):
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        # 예를 들어, 인증 코드의 유효 시간을 1시간으로 설정
        return self.created_at < (datetime.datetime.now() - datetime.timedelta(hours=1))
