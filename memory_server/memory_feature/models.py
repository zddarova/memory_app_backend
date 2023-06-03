from django.db import models

class Memory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    uuid = models.CharField(max_length=36)

    def __str__(self):
        return self.title