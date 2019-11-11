from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model() # 현재 활성화된 모델 가져와줌
        fields = ('first_name', 'last_name')