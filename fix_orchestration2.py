with open("backend/core/orchestration.py", "r") as f:
    content = f.read()

content = content.replace("def undo_log_activity(context: FamilyActionContext):", "def undo_log_activity(context: ExecutionContext):")
content = content.replace("def log_activity(context: FamilyActionContext):", "def log_activity(context: ExecutionContext):")
content = content.replace("def undo_create_event_db(context: FamilyActionContext):", "def undo_create_event_db(context: ExecutionContext):")
content = content.replace("def create_event_db(context: FamilyActionContext):", "def create_event_db(context: ExecutionContext):")
content = content.replace("def undo_create_task_db(context: FamilyActionContext):", "def undo_create_task_db(context: ExecutionContext):")
content = content.replace("def create_task_db(context: FamilyActionContext):", "def create_task_db(context: ExecutionContext):")
content = content.replace("def undo_create_grocery_item_db(context: FamilyActionContext):", "def undo_create_grocery_item_db(context: ExecutionContext):")
content = content.replace("def create_grocery_item_db(context: FamilyActionContext):", "def create_grocery_item_db(context: ExecutionContext):")
content = content.replace("def undo_update_grocery_item_db(context: FamilyActionContext):", "def undo_update_grocery_item_db(context: ExecutionContext):")
content = content.replace("def update_grocery_item_db(context: FamilyActionContext):", "def update_grocery_item_db(context: ExecutionContext):")
content = content.replace("def undo_delete_grocery_item_db(context: FamilyActionContext):", "def undo_delete_grocery_item_db(context: ExecutionContext):")
content = content.replace("def delete_grocery_item_db(context: FamilyActionContext):", "def delete_grocery_item_db(context: ExecutionContext):")

content = content.replace("context.data.data", "context.data")

with open("backend/core/orchestration.py", "w") as f:
    f.write(content)
