import time

LOG_FILE = "ai.log"

def add_log(message):
    timestamp = time.strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {message}"

    with open(LOG_FILE, "a") as f:
        f.write(formatted + "\n")

def reset_log():
    open(LOG_FILE, "w").close()