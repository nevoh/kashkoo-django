from django.db import models

# Create your models here.

class Income(models.Model):
    description = models.CharField(max_length=500)
    annual_amount = models.FloatField()
    start_age = models.IntegerField(null=True, blank=True)
    end_age = models.IntegerField(null=True, blank=True)
    growth =  models.FloatField(null=True, blank=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    
