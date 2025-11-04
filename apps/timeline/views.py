from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json


# === 主畫面（FullCalendar + To-Do 清單）===
def calendar_view(request):
    return render(request, 'timeline/calendar.html')


# === 取得任務清單（供日曆與右側清單載入）===
def task_list(request):
    category = request.GET.get('category')
    tasks = Task.objects.all().order_by('start_date')

    if category and category != "全部":
        tasks = tasks.filter(category=category)

    events = []
    for t in tasks:
        events.append({
            'id': t.id,
            'title': f"{t.title} ({t.category})",
            'start': str(t.start_date),
            'end': str(t.end_date) if t.end_date else str(t.start_date),
            'color': {'學習': '#a78bfa', '工作': '#60a5fa', '生活': '#34d399'}.get(t.category, '#9ca3af'),
            'textColor': '#000000',
            'opacity': 0.6 if t.is_done else 1,
        })
    return JsonResponse(events, safe=False)


# === 新增任務 ===
@csrf_exempt
def add_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Task.objects.create(
            title=data.get('title', ''),
            category=data.get('category', '學習'),
            description=data.get('description', ''),
            start_date=data.get('start'),
            end_date=data.get('end'),
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# === 編輯任務 ===
@csrf_exempt
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        data = json.loads(request.body)
        task.title = data.get('title', task.title)
        task.category = data.get('category', task.category)
        task.description = data.get('description', task.description)
        task.start_date = data.get('start', task.start_date)
        task.end_date = data.get('end', task.end_date)
        task.save()
        return JsonResponse({'status': 'updated'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# === 取得單一任務（用於彈窗編輯）===
def get_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    data = {
        'id': task.id,
        'title': task.title,
        'category': task.category,
        'description': task.description,
        'start_date': str(task.start_date),
        'end_date': str(task.end_date) if task.end_date else "",
        'is_done': task.is_done,
    }
    return JsonResponse(data)


# === 標示完成 / 取消完成 ===
@csrf_exempt
def toggle_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_done = not task.is_done
    task.save()
    return JsonResponse({'status': 'ok', 'is_done': task.is_done})


# === 刪除任務 ===
@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
