import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from trees.models import Tree, Project
from django.db import connection

def check_trees():
    """檢查樹木數據"""
    try:
        trees = Tree.objects.all()
        print(f"成功連接到數據庫!")
        print(f"找到 {len(trees)} 筆樹木記錄:")
        
        # 顯示所有樹木記錄的基本信息
        for tree in trees:
            print(f"ID: {tree._id}, 樹種: {tree.species}")
            print(f"  胸徑: {tree.diameter} cm, 樹高: {tree.height} m")
            print(f"  記錄日期: {tree.record_date}")
            print(f"  項目ID: {tree.project_id}")
            
            # 嘗試獲取關聯的項目
            project = tree.project
            if project:
                print(f"  所屬項目: {project.name} (ID: {project.id})")
            else:
                print(f"  找不到關聯的項目 (項目ID: {tree.project_id})")
            print("")
            
    except Exception as e:
        print(f"錯誤: {e}")

def check_projects():
    """檢查項目數據"""
    try:
        projects = Project.objects.all()
        print(f"找到 {len(projects)} 個項目:")
        
        for project in projects:
            print(f"ID: {project.id}, 名稱: {project.name}")
            print(f"  描述: {project.description}")
            print(f"  開始日期: {project.start_date}, 結束日期: {project.end_date}")
            print("")
            
    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    print("正在檢查樹木數據...\n")
    check_trees()
    
    print("\n正在檢查項目數據...\n")
    check_projects()
    
    print("\n完成!") 