with open("backend/core/api.py", "r") as f:
    content = f.read()

content = content.replace("if outcome.is_success():", "if outcome.status == 'SUCCESS':")

with open("backend/core/api.py", "w") as f:
    f.write(content)
