from django.db import models
from django.conf import settings

class Project(models.Model):
    """專案模型"""
    name = models.CharField(max_length=255, verbose_name='專案名稱')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    start_date = models.DateField(null=True, blank=True, verbose_name='開始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='結束日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='創建者',
        related_name='created_projects'
    )

    class Meta:
        db_table = 'trees_project'
        verbose_name = '專案'
        verbose_name_plural = '專案'

    def __str__(self):
        return self.name

class Tree(models.Model):
    """樹木模型"""
    _id = models.AutoField(primary_key=True, db_column='_id')
    species = models.TextField(verbose_name='樹種')
    diameter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='胸徑(cm)')
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='樹高(m)')
    notes = models.TextField(null=True, blank=True, verbose_name='備註')
    record_date = models.DateField(null=True, blank=True, verbose_name='記錄日期')
    project_id = models.IntegerField(null=True, blank=True, verbose_name='專案ID')
    created_at = models.DateField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='創建者',
        related_name='trees'
    )

    class Meta:
        db_table = 'trees'
        verbose_name = '樹木'
        verbose_name_plural = '樹木'

    @property
    def project(self):
        """獲取樹木所屬的專案"""
        return Project.objects.filter(id=self.project_id).first()

    def __str__(self):
        return f'{self._id} - {self.species}'

class TreeHistory(models.Model):
    """樹木歷史記錄模型"""
    tree_id = models.IntegerField(verbose_name='樹木ID')
    action = models.CharField(max_length=20, verbose_name='操作類型')  # 'UPDATE' or 'DELETE'
    species = models.CharField(max_length=100, verbose_name='樹種')
    diameter = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='胸徑(cm)')
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='樹高(m)')
    record_date = models.DateField(verbose_name='記錄日期')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, verbose_name='專案')
    notes = models.TextField(null=True, blank=True, verbose_name='備註')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '樹木歷史記錄'
        verbose_name_plural = '樹木歷史記錄'

    def __str__(self):
        return f"{self.species} - ID: {self.tree_id} - {self.action}"

class TreeImage(models.Model):
    """樹木圖片模型"""
    tree = models.ForeignKey(Tree, related_name='images', on_delete=models.CASCADE, verbose_name='樹木')
    image = models.ImageField(upload_to='tree_images/', verbose_name='圖片')
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name='說明')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上傳時間')

    class Meta:
        db_table = 'trees_treeimage'
        verbose_name = '樹木圖片'
        verbose_name_plural = '樹木圖片'

    def __str__(self):
        return f'{self.tree.species} - {self.id}' 