from django.db import models

# Create your models here.
class pdf(models.Model):
    file = models.FileField(upload_to="pdfs/")
    summary = models.TextField(blank = True)
    audio = models.FileField(upload_to="audios/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank = True)

    def __str__(self):
        return self.file.name