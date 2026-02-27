from plane.core_mp import connect_tcp, arm, gps_lock, set_mode, PositionController
from ai.trustlogic import TrustManager
from plane.gesturemovement import BehaviorMovement
from cv.camera import get_stable_input, end_cam
from msg.log import get_logs
import time

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

    except KeyboardInterrupt:
        print("Program ended.")

    finally:
        end_cam()

if __name__ == "__main__":
    main()
