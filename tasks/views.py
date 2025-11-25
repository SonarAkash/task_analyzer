import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Task
from .scoring import TaskScorer
from django.shortcuts import render

@csrf_exempt
@require_http_methods(["POST"])
def analyze_tasks(request):
    """
    API Endpoint: Accepts a list of tasks (JSON), calculates scores, 
    and returns them sorted by priority.
    """
    try:
        data = json.loads(request.body)
        raw_tasks = data.get('tasks', [])
        strategy = data.get('strategy', 'balanced')

        # Convert raw JSON data into Task objects,in-memory only
        task_objects = []
        for item in raw_tasks:
            due_date = None
            if item.get('due_date'):
                try:
                    due_date = datetime.strptime(item['due_date'], '%Y-%m-%d').date()
                except ValueError:
                    pass # Keep None if invalid date

            task = Task(
                id=item.get('id'),
                title=item.get('title', 'Untitled'),
                due_date=due_date,
                importance=int(item.get('importance', 1)),
                estimated_hours=float(item.get('estimated_hours', 1.0))
            )
            
            # Mock the dependency count
            dependencies = item.get('dependencies', [])
            task.blocking_count_cache = len(dependencies) 
            
            task_objects.append(task)

        sorted_results = TaskScorer.analyze_tasks(task_objects, strategy)

        return JsonResponse({
            'status': 'success',
            'strategy_used': strategy,
            'tasks': sorted_results
        })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

def index(request):
    """
    Renders the main dashboard.
    """
    return render(request, 'tasks/index.html')