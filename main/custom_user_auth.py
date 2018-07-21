from .models import User

class CustomUserAuthentication:
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        if user is not None:
            try:
                user = User.objects.get(password=password)
            except User.DoesNotExist:
                return None
            return user
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
