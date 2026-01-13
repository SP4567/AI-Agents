import datetime

def log(action, user="AI"):
    with open("audit.log", "a") as f:
        f.write(f"{datetime.datetime.utcnow()} | {user} | {action}\n")
