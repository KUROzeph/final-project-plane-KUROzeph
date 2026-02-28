from ultralytics import YOLO
import cv2
import time
from collections import Counter
from src.ai.trustlogic import TrustManager

model = YOLO("model/final_gesture.pt")
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

GESTURE_BUFFER_SIZE = 10
FACE_BUFFER_SIZE = 10
GESTURE_STABLE_THRESHOLD = 3
CONF_THRESHOLD = 0.7

gesture_buffer = []
face_buffer = []

stable_gesture = None
stable_face_count = 0

frame_count = 0

last_update = time.time()
UPDATE_INTERVAL = 3.0

def get_stable_input(trust_manager):
    global stable_gesture, stable_face_count, last_update, frame_count

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        return None, 0, trust_manager.get_state()

    frame = cv2.resize(frame, (640, 480))

    frame_count += 1

    results = model(frame, verbose=False)

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

    detected_label = None
    fist_count = 0

    if len(results[0].boxes) > 0:
        for box in results[0].boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if conf > CONF_THRESHOLD:
                if label == "palm":
                    fist_count += 1
                else:
                    detected_label = label

                if fist_count >= 2:
                    detected_label = "double_palm"

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

    annotated = frame.copy()

    if len(results) > 0 and results[0].boxes is not None:
        for box in results[0].boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            if conf > CONF_THRESHOLD:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = model.names[cls_id]

                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 146, 15), 2)
                cv2.putText(
                    annotated,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 146, 15),
                    2
                )

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

    cv2.imshow("FOV", annotated)
    cv2.waitKey(1)

    return stable_gesture, stable_face_count, state

def end_cam():
    cap.release()
    cv2.destroyAllWindows()