from django.db import models
from django.conf import settings



class Document(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        PROCESSING = "Processing", "Processing"
        READY = "Ready", "Ready"
        FAILED = "Failed", "Failed"

    organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/%Y/%m/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    error = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="documents")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    


class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    content = models.TextField()

    class Meta:
        ordering = ["document_id", "index"]