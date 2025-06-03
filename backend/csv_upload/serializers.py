from rest_framework import serializers
from .models import CSVFile, DataRecord

class CSVFileSerializer(serializers.ModelSerializer):
    """CSV文件序列化器"""
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = CSVFile
        fields = ['id', 'title', 'file', 'description', 'user', 'uploaded_at', 'processed']
        read_only_fields = ['uploaded_at', 'processed', 'user']

class DataRecordSerializer(serializers.ModelSerializer):
    """数据记录序列化器"""
    csv_file_title = serializers.ReadOnlyField(source='csv_file.title')
    
    class Meta:
        model = DataRecord
        fields = ['id', 'csv_file', 'csv_file_title', 'field1', 'field2', 'field3', 'field4', 'field5', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class DataRecordCreateSerializer(serializers.ModelSerializer):
    """批量创建数据记录的序列化器"""
    class Meta:
        model = DataRecord
        fields = ['csv_file', 'field1', 'field2', 'field3', 'field4', 'field5'] 