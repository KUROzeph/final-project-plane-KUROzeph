from ultralytics import YOLO
import cv2
import time
from collections import Counter

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

model = YOLO("model/gesture2.pt")
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
trust_manager = TrustManager()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

GESTURE_BUFFER_SIZE = 10
FACE_BUFFER_SIZE = 10
GESTURE_STABLE_THRESHOLD = 6
CONF_THRESHOLD = 0.7

gesture_buffer = []
face_buffer = []

stable_gesture = None
stable_face_count = 0

last_update = time.time()
UPDATE_INTERVAL = 1.0

while True:
    ret, frame = cap.read()
    if not ret:
        break


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(40, 40)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    face_buffer.append(len(faces))
    if len(face_buffer) > FACE_BUFFER_SIZE:
        face_buffer.pop(0)

    stable_face_count = round(sum(face_buffer) / len(face_buffer))

    results = model(frame, verbose=False)

    detected_label = None

    if len(results[0].boxes) > 0:
        for box in results[0].boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            if conf > CONF_THRESHOLD:
                detected_label = model.names[cls_id]
                break

    gesture_buffer.append(detected_label)

    if len(gesture_buffer) > GESTURE_BUFFER_SIZE:
        gesture_buffer.pop(0)

    counted = Counter(gesture_buffer)
    if counted:
        most_common, count = counted.most_common(1)[0]
        if count >= GESTURE_STABLE_THRESHOLD:
            stable_gesture = most_common
        else:
            stable_gesture = None

    annotated = results[0].plot()

    current_time = time.time()

    if current_time - last_update >= UPDATE_INTERVAL:
        trust_manager.update(stable_gesture, stable_face_count)
        last_update = current_time

    state = trust_manager.get_state()

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)

    cv2.putText(
    annotated,
    f"trust: {state['trust']}",
    (20, 40),
    font,
    0.7,
    color,
    2
    )

    cv2.putText(
    annotated,
    f"state: {state['category']}",
    (20, 60),
    font,
    0.7,
    color,
    2
    )

    cv2.putText(
    annotated,
    f"condition: {state['break']}",
    (20, 80),
    font,
    0.7,
    color,
    2
    )


    cv2.imshow("", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()