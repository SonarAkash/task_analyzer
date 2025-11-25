from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Task(models.Model):
    """
    Represents a single unit of work to be analyzed.
    Includes validators to ensure data quality (Importance 1-10).
    """
    title = models.CharField(max_length=200)
    
    # We allow null due_date to handle tasks without strict deadlines
    due_date = models.DateField(null=True, blank=True)
    
    # Using Float to allow "1.5 hours"
    estimated_hours = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="Time required to complete in hours"
    )
    
    # Enforcing 1-10 scale as per requirements
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Priority rating from 1 (low) to 10 (high)"
    )
    
    # Self-referential relationship: A task can depend on other tasks
    dependencies = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        blank=True,
        related_name='blocking'
    )

    def __str__(self):
        return f"{self.title} (Imp: {self.importance})"