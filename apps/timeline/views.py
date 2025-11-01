from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from .models import Task, TaskFile
from datetime import date

# === 主畫面 ===
def timeline_index(request):
    today = date.today()
    tasks = Task.objects.filter(date__month=today.month).order_by("date")
    return render(request, "timeline/index.html", {"tasks": tasks, "today": today})


# === 新增任務 ===
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description", "")
        date_str = request.POST.get("date")
        files = request.FILES.getlist("files")

        user = request.user if request.user.is_authenticated else None

        task = Task.objects.create(
            user=user,
            title=title,
            description=desc,
            date=date_str
        )

        for f in files:
            TaskFile.objects.create(task=task, file=f)

        return redirect("timeline_index")
    return render(request, "timeline/index.html")


# === 修改任務 ===
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description", "")
        task.date = request.POST.get("date")
        task.save()
        return redirect("timeline_index")
    return render(request, "timeline/edit.html", {"task": task})


# === 刪除任務 ===
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("timeline_index")

