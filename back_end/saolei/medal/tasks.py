from django.db import transaction
from django.tasks import task, TaskResultStatus
from django.utils import timezone
from django_tasks_db.models import DBTaskResult

from userprofile.models import UserProfile
from .services import evaluate_player, refresh_player_medals
from .utils import REFRESH_COALESCE_DELAY


@task(priority=1)
def task_refresh_player_medals(user_id: int, video_ids=None, degrade_levels=None, invalidate_once=False, full=False):
    """重算该玩家已经接上的勋章。同一条任务覆盖这一名玩家。"""
    refresh_player_medals(
        user_id, video_ids=video_ids, degrade_levels=degrade_levels, invalidate_once=invalidate_once, full=full,
    )
    return user_id


def enqueue_player_refresh(user_id, video_ids=None, degrade_levels=None, invalidate_once=False, full=False):
    """同一玩家已有一条 READY 的刷新任务时不再插入，只把这次碰到的录像并进那一条。新任务 3 秒后开始；合并不改已有任务的开始时间。"""
    ids = sorted({int(video_id) for video_id in (video_ids or []) if video_id is not None})
    levels = sorted({level for level in (degrade_levels or []) if level})
    if full or not (ids or levels or invalidate_once):
        return _enqueue_player_task(task_refresh_player_medals, user_id, defer=True, full=True)
    kwargs = {'video_ids': ids}
    if levels:
        kwargs['degrade_levels'] = levels
    if invalidate_once:
        kwargs['invalidate_once'] = True
    return _enqueue_player_task(task_refresh_player_medals, user_id, defer=True, **kwargs)


@task(priority=0)
def task_backfill_player_medals(user_id: int):
    """按当前规则补发这一名玩家。优先级低于上传后的刷新。"""
    evaluate_player(user_id)
    return user_id


def enqueue_player_backfill(user_id: int):
    """同一玩家已有一条 READY 的补发任务时不再插入。"""
    return _enqueue_player_task(task_backfill_player_medals, user_id)


def _merge_refresh_kwargs(row, incoming):
    current = dict((row.args_kwargs or {}).get('kwargs') or {})
    if current.get('full') or incoming.get('full'):
        merged = {'full': True}
    else:
        merged = {
            'video_ids': sorted(set(current.get('video_ids') or []) | set(incoming.get('video_ids') or [])),
            'degrade_levels': sorted(set(current.get('degrade_levels') or []) | set(incoming.get('degrade_levels') or [])),
        }
        if current.get('invalidate_once') or incoming.get('invalidate_once'):
            merged['invalidate_once'] = True
        merged = {key: value for key, value in merged.items() if value not in (None, [], False)}
    if merged == current:
        return
    row.args_kwargs = {'args': list((row.args_kwargs or {}).get('args') or []), 'kwargs': merged}
    row.save(update_fields=['args_kwargs'])


def _enqueue_player_task(player_task, user_id, defer=False, **kwargs):
    # Serialize producers for this player, including the empty-queue case.
    with transaction.atomic():
        if not UserProfile.objects.select_for_update().filter(pk=user_id).exists():
            return None
        ready = DBTaskResult.objects.filter(
            task_path=player_task.module_path, status=TaskResultStatus.READY, args_kwargs__args=[user_id],
        )
        if ready.exists():
            if kwargs:
                row = DBTaskResult.objects.select_for_update().filter(
                    task_path=player_task.module_path, status=TaskResultStatus.READY, args_kwargs__args=[user_id],
                ).first()
                if row is not None:
                    _merge_refresh_kwargs(row, kwargs)
            return None
        queued = player_task.using(run_after=timezone.now() + REFRESH_COALESCE_DELAY) if defer else player_task
        if kwargs:
            return queued.enqueue(user_id, **kwargs)
        return queued.enqueue(user_id)
