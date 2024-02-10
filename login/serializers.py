from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 사용자의 기본 정보 추가
        token['id'] = user.id
        token['name'] = user.name
        token['email'] = user.email
        token['nickname'] = user.nickname
        token['user_type'] = user.user_type

        # 사용자 유형에 따른 추가 정보 포함
        if user.user_type == 'e':
            try:
                enterprise = user.enterprise  # '_set' 접미사 제거
                token['enterprise'] = {
                    'company_name': enterprise.company_name,
                    'company_code': enterprise.company_code,
                    'department': enterprise.department,
                    'position': enterprise.position
                }
            except User.enterprise.RelatedObjectDoesNotExist:
                token['enterprise'] = None

        elif user.user_type == 'i':
            try:
                individual = user.individual  # '_set' 접미사 제거
                token['individual'] = {
                    'school': individual.school,
                    'department': individual.department
                }
            except User.individual.RelatedObjectDoesNotExist:
                token['individual'] = None

        return token

