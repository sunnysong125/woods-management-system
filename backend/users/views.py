from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout, authenticate
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer,
    PasswordChangeSerializer
)

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    """只允许管理员用户访问"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

class RegisterView(APIView):
    """用戶註冊視圖"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            # 創建 token
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            return Response({
                'message': '註冊成功',
                'user': user_serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """用户登录视图"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        print("登錄請求數據:", request.data)  # 添加日誌
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(f"嘗試登錄用戶: {username}")  # 添加日誌
            
            user = authenticate(request, username=username, password=password)
            print(f"認證結果: {user}")  # 添加日誌
            
            if user is not None:
                login(request, user)
                # 獲取或創建 token
                token, _ = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(user)
                return Response({
                    'message': '登录成功',
                    'user': user_serializer.data,
                    'token': token.key
                })
            else:
                return Response({
                    'message': '用户名或密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        print("序列化器錯誤:", serializer.errors)  # 添加日誌
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """用户注销视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'message': '注销成功'})

class PasswordChangeView(APIView):
    """密码修改视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            # 检查旧密码是否正确
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': '旧密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 修改密码
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': '密码修改成功'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    """获取当前登录用户信息"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
