import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from trees.models import Project

def add_test_projects():
    """添加測試專案數據"""
    projects = [
        {
            'name': '台北市行道樹調查',
            'description': '台北市主要道路行道樹調查計畫',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31)
        },
        {
            'name': '新北市公園樹木普查',
            'description': '新北市各公園樹木健康狀況調查',
            'start_date': date(2024, 3, 1),
            'end_date': date(2024, 8, 31)
        },
        {
            'name': '桃園市老樹保護',
            'description': '桃園市百年老樹保護計畫',
            'start_date': date(2024, 6, 1),
            'end_date': date(2025, 5, 31)
        }
    ]
    
    for project_data in projects:
        project = Project.objects.create(**project_data)
        print(f'已創建專案: {project.name}')

if __name__ == '__main__':
    add_test_projects() 