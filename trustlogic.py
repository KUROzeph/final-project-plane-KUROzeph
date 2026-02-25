class TrustManager:
    def __init__(self):
        self.trust = 60
        self.in_love = False
        self.category = "NEUTRAL"
        self.love_threshold = 90
        self.collapse_triggered = False

    def update(self, gesture, face_count):
        if self.collapse_triggered:
            return 

        if face_count == 1:
            self.trust += 1
        elif face_count >= 2:
            self.trust -= 3
        elif face_count == 0:
            self.trust -= 2

        if gesture == "heart_gest":
            self.trust += 10
        elif gesture == "thumbs_up":
            self.trust += 3
        elif gesture == "thumbs_down":
            self.trust -= 5

        self.trust = max(0, min(100, self.trust))

        if not self.in_love and self.trust >= self.love_threshold:
            self.in_love = True

        if self.trust <= 0 and self.in_love:
            self.collapse_triggered = True

        self._update_category()

    def _update_category(self):
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

    def get_state(self):
        return {
            "trust": self.trust,
            "category": self.category,
            "break": self.collapse_triggered,
        }