from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event
import json
from datetime import datetime


# ✅ FullCalendar ↔ Django 時間格式統一
def parse_datetime(dt_str):
    if not dt_str:
        return None

    # FullCalendar 傳進來的格式： "2025-01-10T14:30"
    try:
        return datetime.fromisoformat(dt_str)
    except:
        pass

    # 退而求其次：只傳日期 "2025-01-10"
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d")
    except:
        return None


# ✅ HTML
def personal_calendar(request):
    return render(request, "personal/calendar.html")


# ✅ get_events（完全正確）
def get_events(request):
    events = Event.objects.all().order_by("start")

    data = [
        {
            "id": e.id,
            "title": e.title,
            "start": e.start.isoformat(),
            "end": e.end.isoformat() if e.end else None,
            "backgroundColor": e.display_color,
            "borderColor": e.display_color,
            "textColor": "#1e293b",
            "extendedProps": {
                "note": e.note,
                "tag": e.tag,
                "priority": e.priority,
                "is_completed": e.is_completed,
                "true_color": e.color,
            }
        }
        for e in events
    ]

    return JsonResponse(data, safe=False)


# ✅ add_event（修正時間格式 ✅）
@csrf_exempt
def add_event(request):
    if request.method == "POST":
        data = json.loads(request.body)

        start = parse_datetime(data.get("start"))
        end = parse_datetime(data.get("end")) or start

        Event.objects.create(
            title=data.get("title"),
            start=start,
            end=end,
            color=data.get("color", "#93c5fd"),
            note=data.get("note", ""),
            tag=data.get("tag", ""),
            priority=data.get("priority", "中"),
        )

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


# ✅ update_event（修正時間格式 ✅）
@csrf_exempt
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        data = json.loads(request.body)

        event.title = data.get("title", event.title)
        event.start = parse_datetime(data.get("start")) or event.start
        event.end = parse_datetime(data.get("end")) or event.end
        event.color = data.get("color", event.color)
        event.note = data.get("note", event.note)
        event.priority = data.get("priority", event.priority)

        event.save()
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


# ✅ delete_event 不動
@csrf_exempt
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return JsonResponse({"status": "ok"})


# ✅ 勾選完成
@csrf_exempt
def toggle_complete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.is_completed = not event.is_completed
    event.save()
    return JsonResponse({
        "status": "ok",
        "completed": event.is_completed,
        "new_color": event.display_color,
    })



