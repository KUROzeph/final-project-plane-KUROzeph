import random

class BehaviorMovement:
    def __init__(self, trust_manager, mp_core):
        self.trust_manager = trust_manager
        self.mp_core = mp_core

    def execute_gesture(self, direction):
        state = self.trust_manager.get_state()
        category = state["category"]
        trust = state["trust"]

        self.do_normal(direction)

    def do_normal(self, direction):
        meters = 200 

        if direction == "point_north":
            self.mp_core.go_north(meters)
        elif direction == "point_south":
            self.mp_core.go_south(meters)
        elif direction == "point_east":
            self.mp_core.go_east(meters)
        elif direction == "point_west":
            self.mp_core.go_west(meters)
