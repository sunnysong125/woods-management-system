from rest_framework import serializers
from .models import Tree, TreeImage, Project, TreeHistory

class ProjectSerializer(serializers.ModelSerializer):
    """專案序列化器"""
    created_by_name = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'created_at', 'updated_at', 'created_by', 'created_by_name', 'created_by_id']
        extra_kwargs = {
            'created_by': {'read_only': True}  # 創建者字段只讀，由視圖自動設置
        }
    
    def get_created_by_name(self, obj):
        """獲取創建者名稱"""
        if obj.created_by:
            return obj.created_by.username
        return None
    
    def get_created_by_id(self, obj):
        """獲取創建者ID"""
        if obj.created_by:
            return obj.created_by.id
        return None

class TreeImageSerializer(serializers.ModelSerializer):
    """樹木圖片序列化器"""
    class Meta:
        model = TreeImage
        fields = ['id', 'image', 'caption', 'uploaded_at']

class TreeSerializer(serializers.ModelSerializer):
    """樹木序列化器"""
    images = TreeImageSerializer(many=True, read_only=True)
    project_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Tree
        fields = [
            '_id', 'species', 'diameter', 'height', 'notes', 'record_date',
            'project_id', 'project_name', 'created_at', 'updated_at', 'images',
            'created_by_name', 'created_by_id'
        ]
    
    def get_project_name(self, obj):
        """獲取樹木所屬專案名稱"""
        project = obj.project
        return project.name if project else None
    
    def get_created_by_name(self, obj):
        """獲取創建者名稱"""
        if obj.created_by:
            return obj.created_by.username
        return None
    
    def get_created_by_id(self, obj):
        """獲取創建者ID"""
        if obj.created_by:
            return obj.created_by.id
        return None

class TreeHistorySerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = TreeHistory
        fields = ['id', 'tree_id', 'action', 'species', 'diameter', 'height', 
                 'record_date', 'project_name', 'notes', 'created_at'] 