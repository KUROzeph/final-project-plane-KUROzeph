from ultralytics import YOLO
import cv2
import time
from collections import Counter


model = YOLO("model/gesture2.pt")
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

GESTURE_BUFFER_SIZE = 10
FACE_BUFFER_SIZE = 10
GESTURE_STABLE_THRESHOLD = 6
CONF_THRESHOLD = 0.7

gesture_buffer = []
face_buffer = []

stable_gesture = None
stable_face_count = 0

last_update = time.time()
UPDATE_INTERVAL = 0.3  

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

    cv2.imshow("", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()