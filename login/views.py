from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status



from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class AccessTokenView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('access_token')
        if not token:
            return Response({'error': '토큰을 받지 못했습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 토큰 검증
            valid_token = AccessToken(token)
            # 토큰 검증 성공, 페이로드 반환
            return Response({'payload': valid_token.payload}, status=status.HTTP_200_OK)
        except Exception as e:
            # 토큰 검증 실패, 401 에러 반환
            return Response({'error': '토큰이 유효하지 않거나 확인할 수 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': '토큰을 받지 못했습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 리프레시 토큰을 검증하고 새로운 액세스 토큰을 발급
            refresh = RefreshToken(refresh_token)
            data = {'access': str(refresh.access_token)}

            # 새로운 액세스 토큰을 응답으로 반환
            return Response(data, status=status.HTTP_200_OK)

        except TokenError as e:
            # 리프레시 토큰이 유효하지 않거나 만료된 경우
            return Response({'error': '토큰이 유효하지 않거나 확인할 수 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)