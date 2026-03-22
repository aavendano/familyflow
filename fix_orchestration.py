with open("backend/core/orchestration.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "context = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'event_data': event_data})" in line:
        line = "    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'event_data': event_data})\n    context = ExecutionContext(data=data)\n"
    elif "context = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'task_data': task_data})" in line:
        line = "    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'task_data': task_data})\n    context = ExecutionContext(data=data)\n"
    elif "context = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_data': item_data})" in line:
        line = "    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_data': item_data})\n    context = ExecutionContext(data=data)\n"
    elif "context = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_id': item_id, 'update_data': update_data})" in line:
        line = "    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_id': item_id, 'update_data': update_data})\n    context = ExecutionContext(data=data)\n"
    elif "context = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_id': item_id})" in line:
        line = "    data = FamilyActionContext(family_id=family_id, actor_id=actor_id, payload={'item_id': item_id})\n    context = ExecutionContext(data=data)\n"
    elif "class FamilyActionContext(ExecutionContext):" in line:
        line = "class FamilyActionContext(BaseModel):\n"

    # Also update uses of context inside blocks: context.data.family_id instead of context.family_id
    new_lines.append(line)

content = "".join(new_lines)
# Regex replace `context.actor_id` to `context.data.actor_id`
import re
content = re.sub(r'context\.actor_id', 'context.data.actor_id', content)
content = re.sub(r'context\.family_id', 'context.data.family_id', content)
content = re.sub(r'context\.payload', 'context.data.payload', content)
content = re.sub(r'context\.trace_id', 'context.data.trace_id', content)
content = re.sub(r'context\.result', 'context.data.result', content)
content = re.sub(r'FamilyActionContext', 'FamilyActionContext', content) # no op

with open("backend/core/orchestration.py", "w") as f:
    f.write(content)
