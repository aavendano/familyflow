from datetime import datetime
from typing import List, Optional
from ninja import NinjaAPI, Schema
from core.models import User, FamilyGroup, Event, TodoTask, Activity, TodoList, GroceryList
from core.orchestration import create_event_flow, create_task_flow

api = NinjaAPI(title="FamilyFlow API", version="1.0.0")

class ErrorResponse(Schema):
    message: str

class EventSchema(Schema):
    id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_all_day: bool

class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    due_date: Optional[datetime] = None

class ActivitySchema(Schema):
    id: int
    action: str
    entity_type: str
    actor_name: Optional[str]
    created_at: datetime

    @staticmethod
    def resolve_actor_name(obj):
        return obj.actor.first_name if obj.actor else None

@api.get("/families/{family_id}/events/", response=List[EventSchema])
def list_events(request, family_id: int):
    return Event.objects.filter(family_id=family_id).order_by('start_time')

@api.get("/families/{family_id}/tasks/", response=List[TaskSchema])
def list_tasks(request, family_id: int):
    return TodoTask.objects.filter(list__family_id=family_id).order_by('due_date')

@api.get("/families/{family_id}/activities/", response=List[ActivitySchema])
def list_activities(request, family_id: int):
    return Activity.objects.filter(family_id=family_id).order_by('-created_at')[:20]

@api.get("/families/{family_id}/dashboard-summary/")
def get_dashboard_summary(request, family_id: int):
    today = datetime.now().date()
    today_events = Event.objects.filter(family_id=family_id, start_time__date=today).order_by('start_time')
    next_event = today_events.first()

    tasks = TodoTask.objects.filter(list__family_id=family_id)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()

    activities = Activity.objects.filter(family_id=family_id).order_by('-created_at')[:5]

    return {
        "next_event": {
            "id": next_event.id,
            "title": next_event.title,
            "start_time": next_event.start_time,
            "location": next_event.location
        } if next_event else None,
        "tasks": {
            "total": total_tasks,
            "completed": completed_tasks
        },
        "activities": [
            {
                "id": a.id,
                "action": a.action,
                "actor_name": a.actor.first_name if a.actor else "System",
                "entity_type": a.entity_type,
                "created_at": a.created_at
            } for a in activities
        ]
    }

class EventCreateSchema(Schema):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_all_day: bool = False

class TaskCreateSchema(Schema):
    list_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

@api.post("/families/{family_id}/events/", response={201: dict, 400: ErrorResponse})
def create_event(request, family_id: int, payload: EventCreateSchema):
    # Retrieve default user for now (e.g., John Smith seeded with ID 1)
    actor_id = request.user.id if request.user.is_authenticated else 1

    event_data = payload.dict()
    outcome = create_event_flow(family_id, actor_id, event_data)

    if outcome.success:
        return 201, {"message": "Event created successfully", "event": outcome.context.result}
    else:
        return 400, {"message": f"Event creation failed"}

@api.post("/families/{family_id}/tasks/", response={201: dict, 400: ErrorResponse})
def create_task(request, family_id: int, payload: TaskCreateSchema):
    actor_id = request.user.id if request.user.is_authenticated else 1

    task_data = payload.dict()
    outcome = create_task_flow(family_id, actor_id, task_data)

    if outcome.success:
        return 201, {"message": "Task created successfully", "task": outcome.context.result}
    else:
        return 400, {"message": f"Task creation failed"}
