from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import TempEmailVerify
import json
from django.utils import timezone






# Create your views here.
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# 이메일 인증 코드 생성 및 전송 요청 처리





@csrf_exempt
def create_and_send_verification_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']

            # 이메일 주소가 제공되지 않았다면 오류 반환
            if not email:
                return JsonResponse({'error': '이메일 주소를 제공해주세요.'}, status=400)

            # 이메일 중복 확인
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': '이미 사용중인 이메일입니다.'}, status=400)

            # 기존의 인증 코드가 있다면 삭제
            TempEmailVerify.objects.filter(email=email).delete()

            # 새로운 인증 코드 생성 및 저장
            verification_code = get_random_string(length=6, allowed_chars='1234567890')
            TempEmailVerify.objects.create(email=email, verification_code=verification_code)

            # 이메일 전송 로직
            send_mail(
                'PoM 회원가입 이메일 인증 코드',
                f'해당 코드를 입력하세요 : {verification_code}',
                'your_email@example.com',  # 보내는 이메일 주소를 여기에 넣으세요.
                [email],
                fail_silently=False,
            )

            return JsonResponse({'message': '인증 코드가 이메일로 전송되었습니다.'}, status=200)
        except KeyError:
            return JsonResponse({'error': '이메일 주소가 제공되지 않았습니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=405)


@csrf_exempt
def verify_code(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')

        if not email or not code:
            return JsonResponse({'error': '이메일과 코드를 모두 입력해주세요.'}, status=400)

        verification_entry = TempEmailVerify.objects.get(email=email)

        if timezone.now() > verification_entry.created_at + timezone.timedelta(hours=1):
            verification_entry.delete()
            return JsonResponse({'error': '코드가 만료되었습니다.'}, status=410)

        if verification_entry.verification_code == code:
            verification_entry.delete()

            return JsonResponse({'message': '인증에 성공하였습니다. 회원가입을 계속 진행해주세요'}, status=200)

        else:
            return JsonResponse({'error': '코드가 일치하지 않습니다'}, status=400)

    except TempEmailVerify.DoesNotExist:
        return JsonResponse({'error': '유효하지 않은 코드입니다.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': '유효하지 않은 JSON 형식입니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': '서버 오류가 발생했습니다.'}, status=500)



def index(request):
    return HttpResponse("안녕하세요 로그인에 오신것을 환영합니다.")