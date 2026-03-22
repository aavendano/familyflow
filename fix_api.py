with open("backend/core/api.py", "r") as f:
    content = f.read()

content = content.replace("if outcome.success:", "if outcome.is_success():")

with open("backend/core/api.py", "w") as f:
    f.write(content)
