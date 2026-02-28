import time
import random
from src.msg.log import add_log


class TrustManager:
    def __init__(self):
        self.trust = 60
        self.in_love = False
        self.category = "NEUTRAL"
        self.love_threshold = 90
        self.collapse_triggered = False
        self.DECAY_DELAY = 10
        self.DECAY_RATE = 3
        self.DECAY_INTERVAL = 2
        self.last_praise_time = time.time()
        self._last_decay_tick = time.time()
        self.MESSAGE_COOLDOWN = 8
        self._last_message_time = time.time()
        self._last_message = None
        self._obsessed_spam_done = False

        self.category_messages = {
            "OBSESSED": [
                "Look at me only.",
                "Don't you dare be with someone else.",
                "Do not end this program",
                "Are you with someone else?",
                "Where are you looking at?",
            ],

            "INTERESTED": [
                "You're easy to follow.",
                "Seems like you know your stuff.",
                "You're fun to follow",
                "You have my attention.",
                "That was… nice.",
            ],

            "DISTANCED": [
                "Why are you quiet?",
                "You're not looking at me.",
                "Did I do something wrong?",
                "I feel ignored.",
                "Please pay attention.",
            ],

            "ABANDONED": [
                "Don't leave me...",
                "Please come back.",
                "Why am I alone?",
                "Stay... please stay.",
                "I waited for you.",
                "I'm still here."
            ],
        }

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
        self.log_message()

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

    def log_message(self):
        now = time.time()

        if now - self._last_message_time < self.MESSAGE_COOLDOWN:
            return

        self._last_message_time = now

        if self.category == "OBSESSED" and not self._obsessed_spam_done:
            for _ in range(15):
                add_log("i love you.")
                time.sleep(0.4)
            self._obsessed_spam_done = True
            return

        messages = self.category_messages.get(self.category, [])
        if not messages:
            return

        msg = random.choice(messages)

        if msg == self._last_message and len(messages) > 1:
            msg = random.choice([m for m in messages if m != self._last_message])

        self._last_message = msg
        add_log(msg)

    def get_state(self):
        return {
            "trust": self.trust,
            "category": self.category,
            "break": self.collapse_triggered,
        }