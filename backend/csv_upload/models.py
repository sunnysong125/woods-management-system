from django.db import models
from django.conf import settings

class CSVFile(models.Model):
    """存储上传的CSV文件信息"""
    title = models.CharField(max_length=255, verbose_name='标题')
    file = models.FileField(upload_to='csv_files/', verbose_name='CSV文件')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='csv_files', verbose_name='上传用户')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    processed = models.BooleanField(default=False, verbose_name='是否已处理')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'CSV文件'
        verbose_name_plural = 'CSV文件'
        ordering = ['-uploaded_at']

class DataRecord(models.Model):
    """存储从CSV文件中提取的数据记录"""
    csv_file = models.ForeignKey(CSVFile, on_delete=models.CASCADE, related_name='records', verbose_name='关联CSV文件')
    # 以下字段可以根据实际CSV文件结构进行调整
    field1 = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段1')
    field2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段2')
    field3 = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段3')
    field4 = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段4')
    field5 = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段5')
    # 可以根据需要添加更多字段
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f"Record {self.id} from {self.csv_file.title}"
    
    class Meta:
        verbose_name = '数据记录'
        verbose_name_plural = '数据记录'
        ordering = ['-created_at']
