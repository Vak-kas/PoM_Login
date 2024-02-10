from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class account_activation_token(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # 사용자 ID, 타임스탬프, 이메일 인증 상태를 조합하여 해시 값을 생성합니다.
        return (text_type(user.id) + text_type(timestamp) + text_type(user.email))
