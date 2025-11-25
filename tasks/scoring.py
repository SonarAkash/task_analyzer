from datetime import date
from typing import Dict, Any
from .models import Task


class TaskScorer:
    """
    Encapsulates the logic for prioritizing tasks based on multiple factors.
    Implements the Strategy Pattern to allow dynamic re-weighting of priorities.
    """

    # Configuration for different sorting strategies
    # multipliers based on what the user values most
    STRATEGIES = {
        'balanced': {'urgency': 1.5, 'importance': 1.2, 'effort': 0.8, 'dependency': 2.0},
        # Prioritizes low effort
        'fastest':  {'urgency': 0.5, 'importance': 0.5, 'effort': 3.0, 'dependency': 0.5},
        # Prioritizes high importance
        'impact':   {'urgency': 0.5, 'importance': 3.0, 'effort': 0.5, 'dependency': 0.5},
        # Prioritizes due dates
        'deadline': {'urgency': 3.0, 'importance': 0.5, 'effort': 0.5, 'dependency': 1.0},
    }
    @staticmethod
    def calculate_score(task: Task, strategy_name: str = 'balanced') -> float:
        """
        Calculates a priority score for a single task.
        Higher score = Higher priority.
        """
        weights = TaskScorer.STRATEGIES.get(strategy_name, TaskScorer.STRATEGIES['balanced'])
        score = 0.0

        # 1. URGENCY SCORE
        if task.due_date:
            days_until_due = (task.due_date - date.today()).days
            
            # Calculate raw urgency score first
            raw_urgency = 0
            if days_until_due < 0:
                 # Critical: Overdue tasks get massive base points + multiplier per day
                raw_urgency = 100 + (abs(days_until_due) * 5)
            elif days_until_due == 0:
                raw_urgency = 50  # Due today
            else:
                # Score decreases as deadline gets further (max lookahead 30 days)
                raw_urgency = max(0, 30 - days_until_due)
            
            # Strategy Weight to the ENTIRE urgency component
            score += raw_urgency * weights['urgency']
        
        # 2. IMPORTANCE SCORE
        score += task.importance * 10 * weights['importance']

        # 3. EFFORT SCORE (Inverted)
        if task.estimated_hours > 0:
            effort_score = (10 / task.estimated_hours) 
            score += effort_score * weights['effort']

        # 4. DEPENDENCY SCORE
        # The count of tasks this task is BLOCKING
        if hasattr(task, 'blocking_count_cache'):
            # pre-calculated count if available
            dependent_count = task.blocking_count_cache
        elif task.id:
            dependent_count = task.blocking.count()
        else:
            dependent_count = 0
            
        score += dependent_count * 10 * weights['dependency']

        return round(score, 2)

    @staticmethod
    def analyze_tasks(tasks: list[Task], strategy: str = 'balanced') -> list[Dict[str, Any]]:
        """
        Takes a list of task objects, scores them, and returns a sorted list of dictionaries.
        """
        results = []
        for task in tasks:
            score = TaskScorer.calculate_score(task, strategy)
            results.append({
                'id': task.id,
                'title': task.title,
                'due_date': task.due_date,
                'importance': task.importance,
                'estimated_hours': task.estimated_hours,
                'score': score,
                'blocking_count': task.blocking.count()
            })
        
        # Sort by score descending (Highest priority first)
        return sorted(results, key=lambda x: x['score'], reverse=True)