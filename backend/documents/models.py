from django.db import models
from django.conf import settings



class Document(models.Model):
    organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="documents")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
