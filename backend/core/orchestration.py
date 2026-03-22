import uuid
from typing import Optional, Any
from pydantic import BaseModel, Field
from vibeblocks import block, ExecutionContext, FailureStrategy, Flow, SyncRunner

class FamilyActionContext(BaseModel):
    family_id: int
    actor_id: int
    payload: dict = Field(default_factory=dict)
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    result: Optional[Any] = None

def undo_log_activity(context: ExecutionContext):
    from .models import Activity
    activity_id = context.data.payload.get('activity_id')
    if activity_id:
        Activity.objects.filter(id=activity_id).delete()

@block(
    name="log_activity",
    description="Logs an activity to the system trace",
    undo=undo_log_activity
)
def log_activity(context: ExecutionContext):
    from .models import Activity, User, FamilyGroup
    actor = User.objects.get(id=context.data.actor_id)
    family = FamilyGroup.objects.get(id=context.data.family_id)

    activity = Activity.objects.create(
        family=family,
        actor=actor,
        action=context.data.payload.get('action', 'performed an action'),
        entity_type=context.data.payload.get('entity_type', 'System'),
        entity_id=context.data.payload.get('entity_id'),
        trace_id=context.data.trace_id
    )
    context.data.payload['activity_id'] = activity.id
    return activity

def undo_create_event_db(context: ExecutionContext):
    from .models import Event
    event_id = context.data.payload.get('entity_id')
    if event_id:
        Event.objects.filter(id=event_id).delete()

@block(
    name="create_event_db",
    description="Persist Event to database",
    undo=undo_create_event_db
)
def create_event_db(context: ExecutionContext):
    from .models import Event, User, FamilyGroup
    actor = User.objects.get(id=context.data.actor_id)
    family = FamilyGroup.objects.get(id=context.data.family_id)
    event_data = context.data.payload.get('event_data', {})

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

    context.data.payload['entity_id'] = event.id
    context.data.payload['entity_type'] = 'Event'
    context.data.payload['action'] = f"created event '{event.title}'"
    context.data.result = {"event_id": event.id, "title": event.title}
    return event

def create_event_flow(family_id: int, actor_id: int, event_data: dict):
    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'event_data': event_data})
    context = ExecutionContext(data=data)
    flow = Flow(name="create_event_flow", blocks=[create_event_db, log_activity], strategy=FailureStrategy.COMPENSATE)
    runner = SyncRunner()
    return runner.run(flow, context)


def undo_create_task_db(context: ExecutionContext):
    from .models import TodoTask
    task_id = context.data.payload.get('entity_id')
    if task_id:
        TodoTask.objects.filter(id=task_id).delete()

@block(
    name="create_task_db",
    description="Persist Task to database",
    undo=undo_create_task_db
)
def create_task_db(context: ExecutionContext):
    from .models import TodoTask, TodoList, User
    task_data = context.data.payload.get('task_data', {})
    todo_list = TodoList.objects.get(id=task_data['list_id'], family_id=context.data.family_id)

    assignee = User.objects.get(id=task_data['assignee_id']) if task_data.get('assignee_id') else None

    task = TodoTask.objects.create(
        list=todo_list,
        title=task_data['title'],
        description=task_data.get('description'),
        due_date=task_data.get('due_date'),
        assignee=assignee
    )

    context.data.payload['entity_id'] = task.id
    context.data.payload['entity_type'] = 'Task'
    context.data.payload['action'] = f"added task '{task.title}'"
    context.data.result = {"task_id": task.id, "title": task.title}
    return task

def create_task_flow(family_id: int, actor_id: int, task_data: dict):
    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'task_data': task_data})
    context = ExecutionContext(data=data)
    flow = Flow(name="create_task_flow", blocks=[create_task_db, log_activity], strategy=FailureStrategy.COMPENSATE)
    runner = SyncRunner()
    return runner.run(flow, context)


def undo_create_grocery_item_db(context: ExecutionContext):
    from .models import GroceryItem
    item_id = context.data.payload.get('entity_id')
    if item_id:
        GroceryItem.objects.filter(id=item_id).delete()

@block(
    name="create_grocery_item_db",
    description="Persist Grocery Item to database",
    undo=undo_create_grocery_item_db
)
def create_grocery_item_db(context: ExecutionContext):
    from .models import GroceryItem, GroceryList, User
    item_data = context.data.payload.get('item_data', {})

    # Assuming there's only one grocery list per family as per requirement
    grocery_list = GroceryList.objects.get(family_id=context.data.family_id)
    actor = User.objects.get(id=context.data.actor_id)

    item = GroceryItem.objects.create(
        list=grocery_list,
        name=item_data['name'],
        quantity=item_data.get('quantity'),
        added_by=actor
    )

    context.data.payload['entity_id'] = item.id
    context.data.payload['entity_type'] = 'Grocery'
    context.data.payload['action'] = f"added grocery item '{item.name}'"
    context.data.result = {"item_id": item.id, "name": item.name}
    return item

def create_grocery_item_flow(family_id: int, actor_id: int, item_data: dict):
    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_data': item_data})
    context = ExecutionContext(data=data)
    flow = Flow(name="create_grocery_item_flow", blocks=[create_grocery_item_db, log_activity], strategy=FailureStrategy.COMPENSATE)
    runner = SyncRunner()
    return runner.run(flow, context)


def undo_update_grocery_item_db(context: ExecutionContext):
    # Updating undo could be restoring previous state, but for simplicity we log the action
    pass

@block(
    name="update_grocery_item_db",
    description="Update Grocery Item in database",
    undo=undo_update_grocery_item_db
)
def update_grocery_item_db(context: ExecutionContext):
    from .models import GroceryItem, User
    item_id = context.data.payload.get('item_id')
    update_data = context.data.payload.get('update_data', {})

    item = GroceryItem.objects.get(id=item_id, list__family_id=context.data.family_id)

    if 'is_purchased' in update_data:
        item.is_purchased = update_data['is_purchased']
    if 'name' in update_data:
        item.name = update_data['name']
    if 'quantity' in update_data:
        item.quantity = update_data['quantity']

    item.save()

    context.data.payload['entity_id'] = item.id
    context.data.payload['entity_type'] = 'Grocery'

    action_text = f"updated grocery item '{item.name}'"
    if 'is_purchased' in update_data:
        if update_data['is_purchased']:
            action_text = f"purchased grocery item '{item.name}'"
        else:
            action_text = f"unmarked grocery item '{item.name}'"

    context.data.payload['action'] = action_text
    context.data.result = {"item_id": item.id, "name": item.name, "is_purchased": item.is_purchased}
    return item

def update_grocery_item_flow(family_id: int, actor_id: int, item_id: int, update_data: dict):
    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_id': item_id, 'update_data': update_data})
    context = ExecutionContext(data=data)
    flow = Flow(name="update_grocery_item_flow", blocks=[update_grocery_item_db, log_activity], strategy=FailureStrategy.COMPENSATE)
    runner = SyncRunner()
    return runner.run(flow, context)


def undo_delete_grocery_item_db(context: ExecutionContext):
    pass

@block(
    name="delete_grocery_item_db",
    description="Delete Grocery Item from database",
    undo=undo_delete_grocery_item_db
)
def delete_grocery_item_db(context: ExecutionContext):
    from .models import GroceryItem
    item_id = context.data.payload.get('item_id')

    item = GroceryItem.objects.get(id=item_id, list__family_id=context.data.family_id)
    item_name = item.name
    item.delete()

    context.data.payload['entity_id'] = item_id
    context.data.payload['entity_type'] = 'Grocery'
    context.data.payload['action'] = f"deleted grocery item '{item_name}'"
    context.data.result = {"success": True}
    return True

def delete_grocery_item_flow(family_id: int, actor_id: int, item_id: int):
    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_id': item_id})
    context = ExecutionContext(data=data)
    flow = Flow(name="delete_grocery_item_flow", blocks=[delete_grocery_item_db, log_activity], strategy=FailureStrategy.COMPENSATE)
    runner = SyncRunner()
    return runner.run(flow, context)
