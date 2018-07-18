from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, password=None,**extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=self.normalize_email(email),
                          nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname, **extra_fields):
        user = self.create_user(email, password=password, nickname=nickname)
        user.is_admin = True
        user.save(using=self._db)
        return user
