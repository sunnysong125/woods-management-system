from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 使用者角色選擇
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', '管理員'
        MEMBER = 'MEMBER', '註冊會員'
    
    # 預設角色為註冊會員
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
        verbose_name='使用者角色'
    )
    
    # 額外的使用者資訊欄位
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='電話號碼')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    
    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_member(self):
        return self.role == self.Role.MEMBER
