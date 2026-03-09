import uuid
from typing import Optional, Any
from pydantic import BaseModel, Field
from vibeblocks import block, ExecutionContext, FailureStrategy, Flow, SyncRunner

class FamilyActionContext(ExecutionContext):
    family_id: int
    actor_id: int
    payload: dict = Field(default_factory=dict)
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    result: Optional[Any] = None

def undo_log_activity(context: FamilyActionContext):
    from .models import Activity
    activity_id = context.payload.get('activity_id')
    if activity_id:
        Activity.objects.filter(id=activity_id).delete()

@block(
    name="log_activity",
    description="Logs an activity to the system trace",
    undo=undo_log_activity
)
def log_activity(context: FamilyActionContext):
    from .models import Activity, User, FamilyGroup
    actor = User.objects.get(id=context.actor_id)
    family = FamilyGroup.objects.get(id=context.family_id)

    activity = Activity.objects.create(
        family=family,
        actor=actor,
        action=context.payload.get('action', 'performed an action'),
        entity_type=context.payload.get('entity_type', 'System'),
        entity_id=context.payload.get('entity_id'),
        trace_id=context.trace_id
    )
    context.payload['activity_id'] = activity.id
    return activity

def undo_create_event_db(context: FamilyActionContext):
    from .models import Event
    event_id = context.payload.get('entity_id')
    if event_id:
        Event.objects.filter(id=event_id).delete()

@block(
    name="create_event_db",
    description="Persist Event to database",
    undo=undo_create_event_db
)
def create_event_db(context: FamilyActionContext):
    from .models import Event, User, FamilyGroup
    actor = User.objects.get(id=context.actor_id)
    family = FamilyGroup.objects.get(id=context.family_id)
    event_data = context.payload.get('event_data', {})

    event = Event.objects.create(
        family=family,
        creator=actor,
        title=event_data['title'],
        start_time=event_data['start_time'],
        end_time=event_data['end_time'],
        description=event_data.get('description'),
        location=event_data.get('location'),
        is_all_day=event_data.get('is_all_day', False)
    )

    context.payload['entity_id'] = event.id
    context.payload['entity_type'] = 'Event'
    context.payload['action'] = f"created event '{event.title}'"
    context.result = {"event_id": event.id, "title": event.title}
    return event

def create_event_flow(family_id: int, actor_id: int, event_data: dict):
    context = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'event_data': event_data})
    flow = Flow(name="create_event_flow", blocks=[create_event_db, log_activity], strategy=FailureStrategy.COMPENSATE)
    runner = SyncRunner(flow)
    return runner.run(context)

def undo_create_task_db(context: FamilyActionContext):
    from .models import TodoTask
    task_id = context.payload.get('entity_id')
    if task_id:
        TodoTask.objects.filter(id=task_id).delete()

@block(
    name="create_task_db",
    description="Persist Task to database",
    undo=undo_create_task_db
)
def create_task_db(context: FamilyActionContext):
    from .models import TodoTask, TodoList, User
    task_data = context.payload.get('task_data', {})
    todo_list = TodoList.objects.get(id=task_data['list_id'], family_id=context.family_id)

    assignee = User.objects.get(id=task_data['assignee_id']) if task_data.get('assignee_id') else None

    task = TodoTask.objects.create(
        list=todo_list,
        title=task_data['title'],
        description=task_data.get('description'),
        due_date=task_data.get('due_date'),
        assignee=assignee
    )

    context.payload['entity_id'] = task.id
    context.payload['entity_type'] = 'Task'
    context.payload['action'] = f"added task '{task.title}'"
    context.result = {"task_id": task.id, "title": task.title}
    return task

def create_task_flow(family_id: int, actor_id: int, task_data: dict):
    context = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'task_data': task_data})
    flow = Flow(name="create_task_flow", blocks=[create_task_db, log_activity], strategy=FailureStrategy.COMPENSATE)
    runner = SyncRunner(flow)
    return runner.run(context)
