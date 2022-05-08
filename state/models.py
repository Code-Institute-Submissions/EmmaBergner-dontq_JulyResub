from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class State(models.Model):
    business = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nr_queue")
    current = models.IntegerField(default=0)

    class Meta:
        ordering = ['-current']

    def __str__(self):
        return f"State for {self.business} currently at {self.current}"
