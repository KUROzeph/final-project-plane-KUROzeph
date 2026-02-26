import random
import time

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
            self.mp_core.go_north(meters)
        elif direction == "point_south":
            self.mp_core.go_south(meters)
        elif direction == "point_east":
            self.mp_core.go_east(meters)
        elif direction == "point_west":
            self.mp_core.go_west(meters)

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

        self.move(direction, meters)

    def do_distanced(self, direction):
        time.sleep(0.8)

        meters = random.randint(200, 250)

        self.move(direction, meters)

    def do_interested(self, direction):
        meters = 300

        self.move(direction, meters)

    def do_obsessed(self, direction):
        meters = random.randint(350, 500)

        if random.random() < 0.3:
            meters += 200
            
        self.move(direction, meters)

    def do_broken(self, direction):
        self.mp_core.fly_to_home()
        self.mp_core.crash()
    
