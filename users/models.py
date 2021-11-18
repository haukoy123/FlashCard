from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, UserManager



class User(AbstractBaseUser):  # REVIEW: thừa kế  AbstractUser thì đỡ phải sửa nhiều hơn
    USERNAME_FIELD = "username"
    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar_url = models.FileField(null=True, upload_to='images/', blank=True)
    is_staff = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        db_table = "user"
    