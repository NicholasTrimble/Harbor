from django.db import models

# Create your models here.
from django.db import models

class Pipeline(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    source_url = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)
    schedule_interval = models.CharField(
        max_length=50, 
        help_text="e.g., '15_min', 'hourly', 'daily'"
    )
    last_run_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PipelineRun(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PARTIAL', 'Partial Success'),
    ]

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='runs')
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FAILED')
    
    # Ingestion Metrics
    records_processed = models.IntegerField(default=0)
    retry_count = models.IntegerField(default=0)
    
    # Error Handling & Observability
    error_message = models.TextField(null=True, blank=True)
    
    # Store structured schema validation failures or drift anomalies
    drift_details = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.pipeline.name} - {self.status} ({self.started_at.strftime('%Y-%m-%d %H:%M')})"