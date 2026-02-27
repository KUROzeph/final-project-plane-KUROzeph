import time

log_messages = []
MAX_LOG_LINES = 20

class logger:
    def add_log(message):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"

        log_messages.append(formatted)

        if len(log_messages) > MAX_LOG_LINES:
            log_messages.pop(0)

    def get_logs():
        return log_messages