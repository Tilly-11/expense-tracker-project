from django.db import models
from django.conf import settings

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)  # user-chosen category
    date = models.DateField()
    predicted_category = models.CharField(max_length=100, blank=True)  # AI prediction
    ai_confidence = models.FloatField(null=True, blank=True)
    user_override = models.BooleanField(default=False)  # did user manually override AI?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user} - {self.amount} on {self.date} ({self.category or self.predicted_category})"