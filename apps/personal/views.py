from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .models import Event
from .tasks import recompute_event_stats

import json
from datetime import datetime


# ======================================================
# 日期解析（統一前後端格式）
# ======================================================
def parse_datetime(dt_str):
    if not dt_str:
        return None

    # YYYY-MM-DD HH:MM
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except:
        pass

    # YYYY-MM-DD
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d")
    except:
        return None


# ======================================================
# 個人行事曆頁面
# ======================================================
@login_required
def personal_calendar(request):
    return render(request, "personal/calendar.html")


# ======================================================
# Events API（FullCalendar 使用 + Redis cache）
# ======================================================
@login_required
def get_events(request):
    cache_key = f"calendar_events_user_{request.user.id}"
    cached = cache.get(cache_key)

    if cached:
        return JsonResponse(cached, safe=False)

    events = Event.objects.filter(user=request.user).order_by("start")
    data = []

    for e in events:
        data.append({
            "id": e.id,
            "title": e.title,
            "start": e.start.strftime("%Y-%m-%dT%H:%M"),
            "end": e.end.strftime("%Y-%m-%dT%H:%M") if e.end else None,
            "backgroundColor": e.display_color,
            "borderColor": e.display_color,
            "textColor": "#1e293b",
            "extendedProps": {
                "note": e.note,
                "priority": e.priority,
                "is_completed": e.is_completed,
                "true_color": e.color,
            },
        })

    cache.set(cache_key, data, timeout=60)
    return JsonResponse(data, safe=False)


# ======================================================
# Chart.js 統計 API（Celery + Cache）
# ======================================================
@login_required
def event_stats(request):
    cache_key = f"event_stats_user_{request.user.id}"
    data = cache.get(cache_key)

    if not data:
        # 非同步丟給 Celery，不阻塞頁面
        recompute_event_stats.delay(request.user.id)
        return JsonResponse({"status": "processing"})

    return JsonResponse(data)


# ======================================================
# 新增事件
# ======================================================
@csrf_exempt
@login_required
def add_event(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)

    start = parse_datetime(data.get("start"))
    end = parse_datetime(data.get("end")) or start

    Event.objects.create(
        user=request.user,
        title=data.get("title"),
        start=start,
        end=end,
        color=data.get("color", "#93c5fd"),
        note=data.get("note", ""),
        priority=data.get("priority", "中"),
    )

    _invalidate(request.user.id)
    return JsonResponse({"success": True})


# ======================================================
# 更新事件
# ======================================================
@csrf_exempt
@login_required
def update_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({"success": False})

    event = get_object_or_404(Event, id=event_id, user=request.user)
    data = json.loads(request.body)

    event.title = data.get("title", event.title)
    event.start = parse_datetime(data.get("start")) or event.start
    event.end = parse_datetime(data.get("end")) or event.end
    event.color = data.get("color", event.color)
    event.note = data.get("note", event.note)
    event.priority = data.get("priority", event.priority)
    event.save()

    _invalidate(request.user.id)
    return JsonResponse({"success": True})


# ======================================================
# 刪除事件
# ======================================================
@csrf_exempt
@login_required
def delete_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({"success": False})

    event = get_object_or_404(Event, id=event_id, user=request.user)
    event.delete()

    _invalidate(request.user.id)
    return JsonResponse({"success": True})


# ======================================================
# 切換完成狀態
# ======================================================
@csrf_exempt
@login_required
def toggle_complete(request, event_id):
    if request.method != "POST":
        return JsonResponse({"success": False})

    event = get_object_or_404(Event, id=event_id, user=request.user)
    event.is_completed = not event.is_completed
    event.save()

    _invalidate(request.user.id)
    return JsonResponse({"success": True})


# ======================================================
# 共用：清除 Cache + 觸發 Celery
# ======================================================
def _invalidate(user_id):
    cache.delete(f"calendar_events_user_{user_id}")
    cache.delete(f"event_stats_user_{user_id}")

    try:
        recompute_event_stats.delay(user_id)
    except Exception as e:
        # production-safe：避免 Celery 掛掉拖垮整個 request
        print(f"[WARN] Celery unavailable: {e}")






