with open("backend/core/orchestration.py", "r") as f:
    content = f.read()

content = content.replace("context = ExecutionContext(data=data)\n    flow = Flow(name=", "context = ExecutionContext(data=data)\n    flow = Flow(name=")

with open("backend/core/orchestration.py", "w") as f:
    f.write(content)
