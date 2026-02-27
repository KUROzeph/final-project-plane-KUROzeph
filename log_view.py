import time
import os

LOG_FILE = "ai.log"

open(LOG_FILE, "a").close()

with open(LOG_FILE, "r") as f:
    f.seek(0, os.SEEK_END)

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.2)
            continue
        print(line.strip())