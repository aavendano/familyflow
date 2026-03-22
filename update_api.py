import re

with open("backend/core/api.py", "r") as f:
    content = f.read()

# Add imports to top
new_imports = "from core.models import User, FamilyGroup, Event, TodoTask, Activity, TodoList, GroceryList, GroceryItem\nfrom core.orchestration import create_event_flow, create_task_flow, create_grocery_item_flow, update_grocery_item_flow, delete_grocery_item_flow\n"
content = re.sub(r'from core\.models.*?\nfrom core\.orchestration.*?\n', new_imports, content, count=1)

# Add Grocery schemas
schemas = """
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

"""

content = content.replace("class TaskSchema(Schema):", schemas + "class TaskSchema(Schema):")

# Add Grocery endpoints
grocery_endpoints = """
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

    if outcome.success:
        return 201, {"message": "Grocery item created successfully", "item": outcome.context.result}
    else:
        return 400, {"message": f"Grocery item creation failed"}

@api.put("/families/{family_id}/groceries/{item_id}", response={200: dict, 400: ErrorResponse, 404: ErrorResponse})
def update_grocery_item(request, family_id: int, item_id: int, payload: GroceryItemUpdateSchema):
    actor_id = request.user.id if request.user.is_authenticated else 1

    update_data = payload.dict(exclude_unset=True)
    if not update_data:
         return 400, {"message": "No data provided for update"}

    outcome = update_grocery_item_flow(family_id, actor_id, item_id, update_data)

    if outcome.success:
        return 200, {"message": "Grocery item updated successfully", "item": outcome.context.result}
    else:
        return 400, {"message": f"Grocery item update failed"}

@api.delete("/families/{family_id}/groceries/{item_id}", response={200: dict, 400: ErrorResponse, 404: ErrorResponse})
def delete_grocery_item(request, family_id: int, item_id: int):
    actor_id = request.user.id if request.user.is_authenticated else 1

    outcome = delete_grocery_item_flow(family_id, actor_id, item_id)

    if outcome.success:
        return 200, {"message": "Grocery item deleted successfully"}
    else:
        return 400, {"message": f"Grocery item deletion failed"}

"""

# Add endpoints before create_event
content = content.replace("class EventCreateSchema", grocery_endpoints + "class EventCreateSchema")


# Update dashboard stats
dashboard_update = """
    groceries = GroceryItem.objects.filter(list__family_id=family_id)
    total_groceries = groceries.count()
    completed_groceries = groceries.filter(is_purchased=True).count()
"""
content = content.replace("activities = Activity.objects", dashboard_update + "    activities = Activity.objects")

dashboard_stats = """
        "groceries": {
            "total": total_groceries,
            "purchased": completed_groceries
        },
        "tasks": {
"""
content = content.replace('"tasks": {', dashboard_stats)

with open("backend/core/api.py", "w") as f:
    f.write(content)
