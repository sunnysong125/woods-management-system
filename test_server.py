#!/usr/bin/env python
"""
🧪 後端服務器測試腳本
用於驗證Django服務器是否能正常啟動
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def test_django_setup():
    """測試Django設置是否正確"""
    try:
        # 設置Django設置模組
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        
        # 初始化Django
        django.setup()
        
        print("✅ Django設置成功")
        
        # 測試導入主要模組
        from users.views import get_csrf_token, LoginView
        print("✅ users.views 導入成功")
        
        from users.urls import urlpatterns
        print("✅ users.urls 導入成功")
        
        # 檢查URL配置
        print(f"✅ 發現 {len(urlpatterns)} 個URL模式")
        
        return True
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def run_check():
    """執行Django檢查"""
    try:
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Django檢查通過")
        return True
    except Exception as e:
        print(f"❌ Django檢查失敗: {e}")
        return False

if __name__ == "__main__":
    print("🧪 開始測試Django後端...")
    print("=" * 50)
    
    # 切換到backend目錄
    if os.path.exists('backend'):
        os.chdir('backend')
        sys.path.insert(0, os.getcwd())
    
    # 測試Django設置
    if test_django_setup():
        print("\n🔍 執行Django系統檢查...")
        if run_check():
            print("\n🎉 所有測試通過！服務器應該可以正常啟動。")
            print("\n📋 建議的啟動命令:")
            print("   python manage.py runserver 0.0.0.0:8085")
        else:
            print("\n⚠️  Django檢查發現問題，請查看上方錯誤信息。")
    else:
        print("\n❌ Django設置失敗，請檢查配置。") 