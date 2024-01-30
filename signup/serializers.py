# serializers.py
from rest_framework import serializers
from .models import User, Individual, Enterprise

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ('company_name', 'department', 'position')

class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ('school', 'department')

class UserSerializer(serializers.ModelSerializer):
    individual = IndividualSerializer(required=False)
    enterprise = EnterpriseSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone', 'birthdate', 'addr', 'sex', 'user_type', 'nickname', 'individual', 'enterprise')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        individual_data = validated_data.pop('individual', None)
        enterprise_data = validated_data.pop('enterprise', None)
        user = User.objects.create_user(**validated_data)

        if user.user_type == 'i' and individual_data:
            Individual.objects.create(user=user, **individual_data)
        elif user.user_type == 'e' and enterprise_data:
            Enterprise.objects.create(user=user, **enterprise_data)

        return user
