import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.users import managers
from apps.users.validators import validate_username


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('staff', 'Staff'),
        ('managers', 'Managers'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    user_type = models.CharField(
        choices=USER_TYPE_CHOICES,
        max_length=16,
        default='staff'
    )
    fullname = models.CharField(_('fullname'), max_length=200, null=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[validate_username],
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_archived = models.BooleanField(default=False)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updated_at = models.DateTimeField(_('date updated'), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["fullname", "email"]
    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])


class StaffUser(User):
    objects = managers.StaffUserManager()

    class Meta:
        proxy = True

    def deactivate_user(self):
        self.is_active = False
        self.updated_at = timezone.now()
        self.save()

    def activate_user(self):
        self.is_active = True
        self.updated_at = timezone.now()
        self.save()


class ManagerUser(User):
    objects = managers.ManagerUserManager()

    class Meta:
        proxy = True

    def deactivate_user(self):
        self.is_active = False
        self.updated_at = timezone.now()
        self.save()

    def activate_user(self):
        self.is_active = True
        self.updated_at = timezone.now()
        self.save()
