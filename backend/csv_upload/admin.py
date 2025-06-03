from django.contrib import admin
from .models import CSVFile, DataRecord

@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at', 'processed')
    list_filter = ('processed', 'uploaded_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('uploaded_at',)

@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'csv_file', 'field1', 'field2', 'created_at')
    list_filter = ('csv_file', 'created_at')
    search_fields = ('field1', 'field2', 'field3', 'field4', 'field5')
    readonly_fields = ('created_at', 'updated_at')
