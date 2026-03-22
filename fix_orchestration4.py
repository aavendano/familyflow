with open("backend/core/orchestration.py", "r") as f:
    content = f.read()

content = content.replace("context = FamilyActionContext(data=data)\n", "context = ExecutionContext(data=data)\n")

with open("backend/core/orchestration.py", "w") as f:
    f.write(content)

with open("backend/core/api.py", "r") as f:
    api_content = f.read()

api_content = api_content.replace("outcome.context.result", "outcome.context.data.result")
with open("backend/core/api.py", "w") as f:
    f.write(api_content)
