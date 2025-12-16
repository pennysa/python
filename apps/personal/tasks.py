from celery import shared_task
from django.core.cache import cache
from django.db.models import Count
from .models import Event


@shared_task
def recompute_event_stats(user_id):
    qs = Event.objects.filter(user_id=user_id)

    total = qs.count()
    completed = qs.filter(is_completed=True).count()

    data = {
        "completion": {
            "completed": completed,
            "pending": total - completed,
        },
        "priority": list(
            qs.values("priority").annotate(count=Count("id"))
        ),
        "tags": list(
            qs.exclude(tag="").values("tag").annotate(count=Count("id"))
        ),
    }

    cache.set(f"event_stats_user_{user_id}", data, timeout=3600)
    return data
