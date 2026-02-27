from plane.core_mp import connect_tcp, arm, gps_lock, set_mode, PositionController
from ai.trustlogic import TrustManager
from plane.gesturemovement import BehaviorMovement
from cv.camera import get_stable_input, end_cam
from msg.log import get_logs
import time
import cv2
import numpy as np

def main():
    master = connect_tcp(host='localhost', port=5763)
    gps_lock(master)
    arm(master)
    set_mode(master, "AUTO")

    time.sleep(10)

    set_mode(master, "GUIDED")

    mp_core = PositionController(master)
    mp_core.initialize()
    trust_manager = TrustManager()
    behavior = BehaviorMovement(trust_manager, mp_core)

    try:
        while True:
            result = get_stable_input(trust_manager)

            if result:
                gesture, faces, state = result

                if gesture:
                    behavior.execute_gesture(gesture)

            terminal = np.zeros((500, 700, 3), dtype=np.uint8)

            logs = get_logs()

            y = 30
            cv2.putText(terminal, "AI TERMINAL", (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

            y += 40

            for log in logs:
                cv2.putText(terminal, log, (20, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)
                y += 25

            cv2.imshow("AI Terminal", terminal)
            cv2.waitKey(1)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program ended.")

    finally:
        end_cam()

if __name__ == "__main__":
    main()
