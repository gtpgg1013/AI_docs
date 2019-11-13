from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model() # 현재 활성화된 모델 가져와줌
        fields = ('first_name', 'last_name', 'email',)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # username, password1, password2, email
        model = get_user_model() # 원래는 auth.User 였을 텐데 accounts.User 참조
        fields = UserCreationForm.Meta.fields + ('email', )