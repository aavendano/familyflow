from datetime import datetime
from typing import List, Optional
from ninja import NinjaAPI, Schema
from core.models import User, FamilyGroup, Event, TodoTask, Activity, TodoList, GroceryList, GroceryItem
from core.orchestration import create_event_flow, create_task_flow, create_grocery_item_flow, update_grocery_item_flow, delete_grocery_item_flow

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


class GroceryItemSchema(Schema):
    id: int
    name: str
    quantity: Optional[str] = None
    is_purchased: bool

class GroceryItemCreateSchema(Schema):
    name: str
    quantity: Optional[str] = None

class GroceryItemUpdateSchema(Schema):
    name: Optional[str] = None
    quantity: Optional[str] = None
    is_purchased: Optional[bool] = None

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
    return Activity.objects.select_related('actor').filter(family_id=family_id).order_by('-created_at')[:20]

@api.get("/families/{family_id}/dashboard-summary/")
def get_dashboard_summary(request, family_id: int):
    today = datetime.now().date()
    today_events = Event.objects.filter(family_id=family_id, start_time__date=today).order_by('start_time')
    next_event = today_events.first()

    tasks = TodoTask.objects.filter(list__family_id=family_id)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()


    groceries = GroceryItem.objects.filter(list__family_id=family_id)
    total_groceries = groceries.count()
    completed_groceries = groceries.filter(is_purchased=True).count()
    activities = Activity.objects.select_related('actor').filter(family_id=family_id).order_by('-created_at')[:5]

    return {
        "next_event": {
            "id": next_event.id,
            "title": next_event.title,
            "start_time": next_event.start_time,
            "location": next_event.location
        } if next_event else None,

        "groceries": {
            "total": total_groceries,
            "purchased": completed_groceries
        },
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


@api.get("/families/{family_id}/groceries/", response=List[GroceryItemSchema])
def list_groceries(request, family_id: int):
    # Retrieve default grocery list
    grocery_list = GroceryList.objects.filter(family_id=family_id).first()
    if not grocery_list:
        return []
    return GroceryItem.objects.filter(list_id=grocery_list.id).order_by('is_purchased', '-created_at')

@api.post("/families/{family_id}/groceries/", response={201: dict, 400: ErrorResponse})
def create_grocery_item(request, family_id: int, payload: GroceryItemCreateSchema):
    actor_id = request.user.id if request.user.is_authenticated else 1

    # Ensure grocery list exists
    grocery_list, created = GroceryList.objects.get_or_create(family_id=family_id, defaults={'name': 'Main List'})

    item_data = payload.dict()
    outcome = create_grocery_item_flow(family_id, actor_id, item_data)

    if outcome.status == 'SUCCESS':
        return 201, {"message": "Grocery item created successfully", "item": outcome.context.data.result}
    else:
        return 400, {"message": f"Grocery item creation failed"}

@api.put("/families/{family_id}/groceries/{item_id}", response={200: dict, 400: ErrorResponse, 404: ErrorResponse})
def update_grocery_item(request, family_id: int, item_id: int, payload: GroceryItemUpdateSchema):
    actor_id = request.user.id if request.user.is_authenticated else 1

    update_data = payload.dict(exclude_unset=True)
    if not update_data:
         return 400, {"message": "No data provided for update"}

    outcome = update_grocery_item_flow(family_id, actor_id, item_id, update_data)

    if outcome.status == 'SUCCESS':
        return 200, {"message": "Grocery item updated successfully", "item": outcome.context.data.result}
    else:
        return 400, {"message": f"Grocery item update failed"}

@api.delete("/families/{family_id}/groceries/{item_id}", response={200: dict, 400: ErrorResponse, 404: ErrorResponse})
def delete_grocery_item(request, family_id: int, item_id: int):
    actor_id = request.user.id if request.user.is_authenticated else 1

    outcome = delete_grocery_item_flow(family_id, actor_id, item_id)

    if outcome.status == 'SUCCESS':
        return 200, {"message": "Grocery item deleted successfully"}
    else:
        return 400, {"message": f"Grocery item deletion failed"}

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

    if outcome.status == 'SUCCESS':
        return 201, {"message": "Event created successfully", "event": outcome.context.data.result}
    else:
        return 400, {"message": f"Event creation failed"}

@api.post("/families/{family_id}/tasks/", response={201: dict, 400: ErrorResponse})
def create_task(request, family_id: int, payload: TaskCreateSchema):
    actor_id = request.user.id if request.user.is_authenticated else 1

    task_data = payload.dict()
    outcome = create_task_flow(family_id, actor_id, task_data)

    if outcome.status == 'SUCCESS':
        return 201, {"message": "Task created successfully", "task": outcome.context.data.result}
    else:
        return 400, {"message": f"Task creation failed"}
