from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout, authenticate
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .models import CustomUser
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer,
    PasswordChangeSerializer
)
import json

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

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    """用户登录视图"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        print("登錄請求數據:", request.data)  # 添加日誌
        print("請求頭:", dict(request.headers))  # 添加請求頭日誌
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(f"嘗試登錄用戶: {username}")  # 添加日誌
            
            user = authenticate(request, username=username, password=password)
            print(f"認證結果: {user}")  # 添加日誌
            
            if user is not None:
                if not user.is_active:
                    return Response({
                        'detail': '用戶帳號已被停用'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
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
                    'detail': '用戶名或密碼錯誤，請重新輸入'
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

# 添加CSRF token獲取端點
@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """獲取CSRF token"""
    return Response({'detail': 'CSRF cookie set'})

# 臨時的CSRF豁免登入視圖（僅用於調試）
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def test_login(request):
    """臨時的CSRF豁免登入視圖（僅用於調試）"""
    print("測試登入請求數據:", request.data)
    print("請求頭:", dict(request.headers))
    print("Origin:", request.META.get('HTTP_ORIGIN', 'None'))
    print("Host:", request.META.get('HTTP_HOST', 'None'))
    
    try:
        data = request.data if hasattr(request, 'data') else json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        print(f"嘗試登錄用戶: {username}")
        
        user = authenticate(request, username=username, password=password)
        print(f"認證結果: {user}")
        
        if user is not None:
            if not user.is_active:
                return JsonResponse({
                    'detail': '用戶帳號已被停用'
                }, status=401)
            
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            return JsonResponse({
                'message': '登录成功',
                'user': user_serializer.data,
                'token': token.key
            })
        else:
            return JsonResponse({
                'detail': '用戶名或密碼錯誤，請重新輸入'
            }, status=401)
    except Exception as e:
        print(f"登入過程中發生錯誤: {e}")
        return JsonResponse({
            'detail': f'登入過程中發生錯誤: {str(e)}'
        }, status=500)
