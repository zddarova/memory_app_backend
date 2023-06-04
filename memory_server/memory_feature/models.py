from django.db import models
from uuid import uuid4


class User(models.Model):
    uuid = models.UUIDField(default=uuid4(), editable=False, unique=True)

class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title
