from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
        #email, password, extra_field를 인자로 받으며, 내부적으로 create_user매서드 호출
        extra_fields.setdefault('is_staff', True) #is_staff 기능 True
        extra_fields.setdefault('is_superuser', True) #슈퍼유저에게 모든 권한을 부여

        return self.create_user(email, password, **extra_fields) #create_user 를 하는데, 관리자 권한 On 되어 있는 상태에서 생성

class User(AbstractBaseUser, PermissionsMixin):
    idx = models.AutoField(primary_key=True, unique=True) #인덱스
    email = models.EmailField(unique=True) #이메일, 아이디로 사용
    name = models.CharField(max_length=50) #이름
    phone = models.CharField(max_length=15) #핸드폰 번호
    birthdate = models.DateField() #생년월일
    addr = models.CharField(max_length=50) #주소
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')]) #성별
    user_type = models.CharField(max_length=10, choices=[('e', 'Enterprise'), ('i', 'Individual')]) #유저 등급
    nickname = models.CharField(max_length=8, unique=True) #닉네임, 별명
    password = models.CharField(max_length=100)  # 비밀번호

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname']  # createsuperuser 관리 명령 사용할 때 추가로 입력 요구하는 필드

    objects = UserManager()

    def __str__(self):
        return self.email  # 필요에 따라 'self.name' 또는 'self.nickname'으로 변경 가능

class Enterprise(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100) #회사명
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
