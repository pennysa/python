from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Event
import json
from datetime import datetime


# ----------------------------------------------------------
#  時間格式處理（FullCalendar → Python）
# ----------------------------------------------------------
def parse_datetime(dt_str):
    if not dt_str:
        return None

    try:
        return datetime.fromisoformat(dt_str)        # e.g. 2025-01-10T14:30
    except:
        pass

    try:
        return datetime.strptime(dt_str, "%Y-%m-%d")  # e.g. 2025-01-10
    except:
        return None


# ----------------------------------------------------------
#  個人行事曆 HTML 頁面
# ----------------------------------------------------------
@login_required
def personal_calendar(request):
    return render(request, "personal/calendar.html")


# ----------------------------------------------------------
#  取得自己的全部事件（FullCalendar 用）
# ----------------------------------------------------------
@login_required
def get_events(request):

    events = Event.objects.filter(user=request.user).order_by("start")

    data = []
    for e in events:
        data.append({
            "id": e.id,
            "title": e.title,
            "start": e.start.isoformat(),
            "end": e.end.isoformat() if e.end else None,
            "backgroundColor": e.display_color,
            "borderColor": e.display_color,
            "textColor": "#1e293b",
            "allDay": True,
            "extendedProps": {
                "note": e.note,
                "tag": e.tag,
                "priority": e.priority,
                "is_completed": e.is_completed,
                "true_color": e.color,
            },
        })

    return JsonResponse(data, safe=False)


# ----------------------------------------------------------
#  新增事件（AJAX）
# ----------------------------------------------------------
@csrf_exempt
@login_required
def add_event(request):

    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)

    start = parse_datetime(data.get("start"))
    end = parse_datetime(data.get("end")) or start

    event = Event.objects.create(
        user=request.user,         # ← 綁定使用者（必須）
        title=data.get("title"),
        start=start,
        end=end,
        color=data.get("color", "#93c5fd"),
        note=data.get("note", ""),
        tag=data.get("tag", ""),
        priority=data.get("priority", "中"),
    )

    # ⭐ 回傳完整事件（FullCalendar 才能立即渲染）
    return JsonResponse({
        "success": True,
        "event": {
            "id": event.id,
            "title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat() if event.end else None,
            "backgroundColor": event.display_color,
            "borderColor": event.display_color,
            "textColor": "#1e293b",
            "allDay": True,
            "extendedProps": {
                "note": event.note,
                "tag": event.tag,
                "priority": event.priority,
                "is_completed": event.is_completed,
                "true_color": event.color,
            },
        }
    })


# ----------------------------------------------------------
#  更新事件（AJAX）
# ----------------------------------------------------------
@csrf_exempt
@login_required
def update_event(request, event_id):

    event = get_object_or_404(Event, id=event_id, user=request.user)  
    # ↑ 限制：只能修改自己的事件

    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)

    event.title = data.get("title", event.title)
    event.start = parse_datetime(data.get("start")) or event.start
    event.end = parse_datetime(data.get("end")) or event.end
    event.color = data.get("color", event.color)
    event.note = data.get("note", event.note)
    event.priority = data.get("priority", event.priority)
    event.save()

    # ⭐ 必須回傳完整事件給前端更新！
    return JsonResponse({
        "success": True,
        "event": {
            "id": event.id,
            "title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat() if event.end else None,
            "backgroundColor": event.display_color,
            "borderColor": event.display_color,
            "textColor": "#1e293b",
            "allDay": True,
            "extendedProps": {
                "note": event.note,
                "tag": event.tag,
                "priority": event.priority,
                "is_completed": event.is_completed,
                "true_color": event.color,
            },
        }
    })


# ----------------------------------------------------------
#  刪除事件（AJAX）
# ----------------------------------------------------------
@csrf_exempt
@login_required
def delete_event(request, event_id):

    if request.method != "POST":
        return JsonResponse({"success": False})

    event = get_object_or_404(Event, id=event_id, user=request.user)
    event.delete()

    return JsonResponse({"success": True})


# ----------------------------------------------------------
#  is_completed 切換（AJAX）
# ----------------------------------------------------------
@csrf_exempt
@login_required
def toggle_complete(request, event_id):

    event = get_object_or_404(Event, id=event_id, user=request.user)

    event.is_completed = not event.is_completed
    event.save()

    return JsonResponse({
        "success": True,
        "completed": event.is_completed,
        "new_color": event.display_color,
    })
