import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def list_tables():
    """列出資料庫中的所有表格"""
    cursor = connection.cursor()
    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    print('資料庫中的表:')
    for table in cursor.fetchall():
        print(f"  - {table[0]}")

    print("\n檢查 'projects' 表是否存在:")
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'projects'
        )
    """)
    exists = cursor.fetchone()[0]
    print(f"  'projects' 表存在: {exists}")

    # 如果專案表有其他名稱，嘗試搜索類似名稱的表
    if not exists:
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name LIKE '%project%'
        """)
        project_tables = cursor.fetchall()
        print("\n找到可能的專案相關表:")
        if project_tables:
            for table in project_tables:
                # 查看表結構
                cursor.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns
                    WHERE table_name = '{table[0]}'
                """)
                print(f"  '{table[0]}'表結構:")
                for column in cursor.fetchall():
                    print(f"    - {column[0]}: {column[1]}")
        else:
            print("\n未找到任何與專案相關的表")

def check_project_table():
    """檢查 trees_project 表的內容"""
    cursor = connection.cursor()
    # 檢查 trees_project 表結構
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns
        WHERE table_name = 'trees_project'
    """)
    print("\ntrees_project 表結構:")
    for column in cursor.fetchall():
        print(f"  - {column[0]}: {column[1]}")

    # 檢查表中的記錄數量
    cursor.execute("SELECT COUNT(*) FROM trees_project")
    count = cursor.fetchone()[0]
    print(f"\n記錄數量: {count}")

    if count > 0:
        # 顯示前 5 筆記錄
        cursor.execute("SELECT * FROM trees_project LIMIT 5")
        records = cursor.fetchall()
        print("\n前 5 筆記錄:")
        for record in records:
            print(f"  - {record}")

if __name__ == '__main__':
    list_tables()
    check_project_table() 