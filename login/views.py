from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # 사용자 정보를 JSON 형식으로 구성
            user_info = {
                'email': user.email,
                'nickname': user.nickname,
                # 추가 필요한 사용자 정보들을 여기에 포함
            }

            # 응답 구성
            response_data = {
                'access_token': access_token,
                'user_info': user_info,
                'message': '환영합니다!'
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 로그인이 필요한 엔드포인트임을 지정
def user_info(request):
    user = request.user

    # 사용자 정보 구성 (필요한 필드 추가 가능)
    user_info = {
        'email': user.email,
        'nickname': user.nickname,
        'id' : user.id,
        # 필요한 추가 정보 포함
    }

    # 응답 데이터 구성
    response_data = {
        'access_token': '',  # 토큰은 이미 로그인 시에 발급되었으므로 빈 문자열
        'user_info': user_info,
        'message': f"{user.nickname} 환영합니다!"
    }

    return Response(response_data, status=status.HTTP_200_OK)