import random
import time
import threading
from src.msg.log import add_log

class BehaviorMovement:
    def __init__(self, trust_manager, mp_core):
        self.trust_manager = trust_manager
        self.mp_core = mp_core
        self.broken = False
        self.busy = False

    def execute_gesture(self, direction):
        if self.busy:
            return
        
        self.busy = True

        state = self.trust_manager.get_state()
        category = state["category"]
        add_log(f"Executing gesture in state {category}")

        try:

            if category == "ABANDONED":
                self.do_abandoned(direction)
            elif category == "DISTANCED":
                self.do_distanced(direction)
            elif category == "INTERESTED":
                self.do_interested(direction)
            elif category == "OBSESSED":
                self.do_obsessed(direction)
            elif category == "BROKEN":
                if not self.broken:
                    self.do_broken(direction)
                    self.broken = True

        finally:
            self.busy = False

    def move(self, direction, meters):
        if direction == "point_north":
            threading.Thread(target=self.mp_core.go_north, args=(meters,), daemon=True).start()
        elif direction == "point_south":
            threading.Thread(target=self.mp_core.go_south, args=(meters,), daemon=True).start()
        elif direction == "point_east":
            threading.Thread(target=self.mp_core.go_east, args=(meters,), daemon=True).start()
        elif direction == "point_west":
            threading.Thread(target=self.mp_core.go_west, args=(meters,), daemon=True).start()

    def do_abandoned (self, direction):
        if random.random() < 0.5:
            return

        time.sleep(1.5)

        meters = random.randint(100, 150)

        if random.random() < 0.2:
            direction = random.choice([
                "point_north", "point_south",
                "point_east", "point_west"
            ])

        add_log(f"ABANDONED, moving {direction} {meters}m")

        self.move(direction, meters)

    def do_distanced(self, direction):
        time.sleep(0.8)

        meters = random.randint(200, 250)
        add_log(f"DISTANCED, moving {direction} {meters}m")

        self.move(direction, meters)

    def do_interested(self, direction):
        meters = 400
        add_log(f"INTERESTED, moving {direction} {meters}m")

        self.move(direction, meters)

    def do_obsessed(self, direction):
        meters = random.randint(500, 800)

        if random.random() < 0.3:
            meters += 200

        add_log(f"OBSESSED, moving {direction} {meters}m")

        self.move(direction, meters)

    def do_broken(self, direction = None):
        self.mp_core.fly_to_home()
        self.mp_core.crash()
    
