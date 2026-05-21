from django.contrib import admin
from .models import Pipeline, PipelineRun

# Register your models here.
@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule_interval', 'is_active', 'last_run_at')
    list_filter = ('is_active', 'schedule_interval')
    search_fields = ('name',)

@admin.register(PipelineRun)
class PipelineRunAdmin(admin.ModelAdmin):
    list_display = ('pipeline', 'status', 'started_at', 'duration_seconds', 'records_processed')
    list_filter = ('status', 'pipeline')
    readonly_fields = ('started_at', 'completed_at', 'duration_seconds', 'error_message', 'drift_details')