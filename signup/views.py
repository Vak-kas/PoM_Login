from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

from .models import *
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import hashlib
import base64

from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


# Create your views here.
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def email_verify(request):
    email = request.POST.get('email')
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': '이미 사용 중인 이메일입니다.'}, status=400)

    # 이메일 주소를 기반으로 간단한 토큰 생성
    token = base64.urlsafe_b64encode(hashlib.sha256(email.encode()).digest()).decode()

    # 이메일 인증 링크 생성
    activation_link = request.build_absolute_uri(
        reverse('activate_email', kwargs={'token': token, 'email': urlsafe_base64_encode(force_bytes(email))}))

    # 이메일 발송
    send_mail(
        '이메일 인증을 완료해주세요',
        f'아래 링크를 클릭하여 이메일 인증을 완료하세요: {activation_link}',
        'whiterose19654@gmail.com',
        [email],
        fail_silently=False,
    )
    return JsonResponse({'message': '인증 메일을 발송하였습니다. 메일을 확인해 주세요.'})


def activate_email(request, token, email):
    decoded_email = force_str(urlsafe_base64_decode(email))
    generated_token = base64.urlsafe_b64encode(hashlib.sha256(decoded_email.encode()).digest()).decode()

    if token == generated_token and not User.objects.filter(email=decoded_email).exists():
        # 이메일 주소가 유효하고 아직 등록되지 않았음을 확인
        return JsonResponse({'message': '이메일이 성공적으로 인증되었습니다. 회원가입을 계속 진행해주세요.'})
    else:
        return JsonResponse({'error': '유효하지 않은 인증 요청입니다.'}, status=400)



def index(request):
    return HttpResponse("안녕하세요 로그인에 오신것을 환영합니다.")