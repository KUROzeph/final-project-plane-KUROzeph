import time

log_messages = []
MAX_LOG_LINES = 20


def add_log(message):
    timestamp = time.strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {message}"

    print(formatted)

    if len(log_messages) > MAX_LOG_LINES:
        log_messages.pop(0)

def get_logs():
    return log_messages