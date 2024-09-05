from django.contrib.auth.base_user import BaseUserManager


class StaffUserManager(BaseUserManager):
    def get_queryset(self):
        return super(StaffUserManager, self).get_queryset().filter(
            user_type='staff'
        )
    def create(self, email, password=None, **kwargs):
        kwargs.update({
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'staff',
            'username': email,
        })
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class ManagerUserManager(BaseUserManager):
    def get_queryset(self):
        return super(ManagerUserManager, self).get_queryset().filter(
            user_type='managers'
        )
    def create(self, email, password=None, **kwargs):
        kwargs.update({
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'manager',
            'username': email,
        })
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
