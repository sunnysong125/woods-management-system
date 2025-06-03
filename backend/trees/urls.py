from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreeViewSet, TreeImageViewSet, ProjectViewSet, generate_qr_code
from django.views.static import serve
import os
from django.conf import settings

# 創建路由器並註冊視圖集
router = DefaultRouter()
router.register(r'trees', TreeViewSet, basename='tree')
router.register(r'tree-images', TreeImageViewSet)
router.register(r'projects', ProjectViewSet)

# 定義下載範例CSV文件的函數
def download_sample_csv(request):
    file_path = os.path.join(settings.BASE_DIR, 'woodsbackend', 'tree_sample.csv')
    return serve(request, os.path.basename(file_path), os.path.dirname(file_path))

# 加回明確的URL配置
urlpatterns = [
    path('', include(router.urls)),
    # 直接映射到upload_csv方法
    path('trees/upload-csv/', TreeViewSet.as_view({'post': 'upload_csv'}), name='tree-csv-upload'),
    path('trees/<int:tree_id>/generate-qr/', generate_qr_code, name='generate-qr-code'),
    # 添加下載範例CSV的URL
    path('tree_sample.csv', download_sample_csv, name='download-tree-sample'),
] 