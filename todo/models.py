from django.db import models
from django.contrib.auth.models import User


class NewUserTodo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    important = models.BooleanField(default=False)

    class Meta:
        ordering = ("title",)
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self):
        return self.title
