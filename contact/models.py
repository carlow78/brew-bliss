from django.db import models
from django.utils import timezone

class ContactUs(models.Model):
    """
    A model for storing user inquiries or feedback submitted through the websites contact form.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} from {self.name}"

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us Entries"
        ordering = ['-created_at']
