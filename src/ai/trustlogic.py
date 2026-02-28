import time
from src.msg.log import add_log


class TrustManager:
    def __init__(self):
        self.trust = 60
        self.in_love = False
        self.category = "NEUTRAL"
        self.love_threshold = 90
        self.collapse_triggered = False
        self.DECAY_DELAY = 10
        self.DECAY_RATE = 1
        self.DECAY_INTERVAL = 2
        self.last_praise_time = time.time()
        self._last_decay_tick = time.time()

    def update(self, gesture, face_count):
        if self.collapse_triggered:
            return

        current_time = time.time()
        positive_event = False

        if face_count == 1:
            self.trust += 1
            positive_event = True
        elif face_count >= 2:
            self.trust -= 5
        elif face_count == 0:
            self.trust -= 3

        if gesture == "heart_gest":
            self.trust += 10
            positive_event = True
        elif gesture == "thumbs_up":
            self.trust += 3
            positive_event = True
        elif gesture == "thumbs_down":
            self.trust -= 5

        if positive_event:
            self.last_praise_time = current_time

        if current_time - self.last_praise_time > self.DECAY_DELAY:
            elapsed = current_time - self._last_decay_tick
            steps = int(elapsed / self.DECAY_INTERVAL)

            if steps > 0:
                self.trust -= steps * self.DECAY_RATE
                self.trust = max(0, self.trust)
                self._last_decay_tick += steps * self.DECAY_INTERVAL

        self.trust = max(0, min(100, self.trust))

        if not self.in_love and self.trust >= self.love_threshold:
            self.in_love = True

        if self.trust <= 0 and self.in_love:
            self.collapse_triggered = True

        self._update_category()

    def _update_category(self):
        old_category = self.category

        if self.trust == 0 and self.in_love:
            self.category = "BROKEN"
        elif self.trust >= 80:
            self.category = "OBSESSED"
        elif self.trust >= 50:
            self.category = "INTERESTED"
        elif self.trust >= 20:
            self.category = "DISTANCED"
        else:
            self.category = "ABANDONED"

        if self.category != old_category:
            add_log(f"Category changed → {self.category}")

            if self.category == "OBSESSED":
                for i in range (25):
                    add_log("i love you.")
                    time.sleep(1)
            elif self.category == "DISTANCED":
                add_log("why are you not paying attention to me?")
            elif self.category == "ABANDONED":
                add_log("don't leave me...")
            elif self.category == "BROKEN":
                add_log("if i cant have you, then none can.")

    def get_state(self):
        return {
            "trust": self.trust,
            "category": self.category,
            "break": self.collapse_triggered,
        }