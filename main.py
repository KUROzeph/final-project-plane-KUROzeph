from src.plane.core_mp import connect_tcp, arm, gps_lock, set_mode, PositionController
from src.ai.trustlogic import TrustManager
from src.plane.gesturemovement import BehaviorMovement
from src.cv.camera import get_stable_input, end_cam
from src.msg.log import reset_log
import time

def main():
    reset_log()
    
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
    last_gesture = None
    last_log_time = 0
    LOG_DELAY = 2

    try:
        while True:
            result = get_stable_input(trust_manager)

            if result:
                gesture, faces, state = result

                if state["category"] == "BROKEN" and not behavior.broken:
                    behavior.do_broken()
                    behavior.broken = True
                    continue

                current_time = time.time()

                if gesture:
                    if gesture != last_gesture or (current_time - last_log_time) > LOG_DELAY:
                        behavior.execute_gesture(gesture)

                        last_gesture = gesture
                        last_log_time = current_time

    except KeyboardInterrupt:
        print("Program ended.")

    finally:
        end_cam()

if __name__ == "__main__":
    main()
