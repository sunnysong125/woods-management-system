from django.contrib import admin
from .models import Tree, TreeImage, Project, TreeHistory

class TreeImageInline(admin.TabularInline):
    model = TreeImage
    extra = 1
    fields = ('image', 'caption')
    verbose_name = '樹木圖片'
    verbose_name_plural = '樹木圖片'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description')
    list_display_links = ('id', 'name')

    def get_list_display(self, request):
        return ['id', 'name', 'start_date', 'end_date', 'created_at']

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('_id', 'species', 'diameter', 'height', 'record_date', 'project_id', 'created_at')
    list_filter = ('species', 'record_date')
    search_fields = ('species', 'notes')
    inlines = [TreeImageInline]
    list_display_links = ('_id', 'species')

    def get_list_display(self, request):
        return [
            ('_id', 'ID'),
            ('species', '樹種'),
            ('diameter', '胸徑(cm)'),
            ('height', '樹高(m)'),
            ('record_date', '記錄日期'),
            ('project_id', '專案ID'),
            ('created_at', '創建時間')
        ]

@admin.register(TreeImage)
class TreeImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'tree', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('tree__species', 'caption')
    list_display_links = ('id', 'tree')

    def get_list_display(self, request):
        return [
            ('id', 'ID'),
            ('tree', '樹木'),
            ('caption', '說明'),
            ('uploaded_at', '上傳時間')
        ]

@admin.register(TreeHistory)
class TreeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'tree_id', 'action', 'species', 'diameter', 'height', 'record_date', 'created_at')
    list_filter = ('action', 'record_date', 'created_at')
    search_fields = ('species', 'notes', 'tree_id')
    readonly_fields = ('tree_id', 'action', 'species', 'diameter', 'height', 'record_date', 'project', 'notes', 'created_at')
    list_display_links = ('id', 'tree_id')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False 