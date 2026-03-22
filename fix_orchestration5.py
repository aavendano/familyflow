with open("backend/core/orchestration.py", "r") as f:
    content = f.read()

content = content.replace("runner = SyncRunner(flow)", "runner = SyncRunner()\n    return runner.run(flow, context)")
content = content.replace("return runner.run(context)", "")
content = content.replace("return runner.run(flow, context)\n\n", "return runner.run(flow, context)\n")
with open("backend/core/orchestration.py", "w") as f:
    f.write(content)
