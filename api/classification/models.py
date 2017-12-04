from django.db import models

# Create your models here.
class Job(models.Model):
    reference_number = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField('created predicted', auto_now_add=True)
    category = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
        return "%s=[%s]", (self.reference_number, self.category)
