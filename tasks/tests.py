from django.test import TestCase
from datetime import date, timedelta
from .models import Task
from .scoring import TaskScorer

class ScoringAlgorithmTests(TestCase):
    def setUp(self):
        # A few sample tasks for testing
        self.urgent_task = Task.objects.create(
            title="Urgent Task",
            due_date=date.today(),
            importance=5,
            estimated_hours=2.0
        )
        self.important_task = Task.objects.create(
            title="Important Task",
            due_date=date.today() + timedelta(days=10),
            importance=10,
            estimated_hours=2.0
        )
        self.quick_task = Task.objects.create(
            title="Quick Task",
            due_date=date.today() + timedelta(days=5),
            importance=5,
            estimated_hours=0.5
        )

    def test_deadline_strategy(self):
        """Test that deadline strategy prioritizes the urgent task."""
        results = TaskScorer.analyze_tasks(Task.objects.all(), 'deadline')
        self.assertEqual(results[0]['title'], "Urgent Task")

    def test_impact_strategy(self):
        """Test that impact strategy prioritizes the high importance task."""
        results = TaskScorer.analyze_tasks(Task.objects.all(), 'impact')
        self.assertEqual(results[0]['title'], "Important Task")

    def test_fastest_strategy(self):
        """Test that fastest strategy prioritizes the low effort task."""
        results = TaskScorer.analyze_tasks(Task.objects.all(), 'fastest')
        self.assertEqual(results[0]['title'], "Quick Task")