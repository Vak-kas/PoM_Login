from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 사용자 정보를 토큰에 추가
        token['id'] = user.id
        token['name'] = user.name
        token['email'] = user.email
        token['nickname'] = user.nickname
        token['user_type'] = user.user_type

        # 사용자 유형에 따른 추가 정보 포함
        if user.user_type == 'e':
            enterprise = user.enterprise_set.first()
            if enterprise:
                token['enterprise'] = {
                    'company_name': enterprise.company_name,
                    'company_code': enterprise.company_code,
                    'department': enterprise.department,
                    'position': enterprise.position
                }
        elif user.user_type == 'i':
            individual = user.individual_set.first()
            if individual:
                token['individual'] = {
                    'school': individual.school,
                    'department': individual.department
                }

        return token
