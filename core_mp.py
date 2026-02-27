
from pymavlink import mavutil
import time
import math

RESULT_MAP = {
    0: 'ACCEPTED',
    1: 'TEMPORARILY_REJECTED',
    2: 'DENIED',
    3: 'UNSUPPORTED',
    4: 'FAILED',
    5: 'IN_PROGRESS',
    }

def connect_tcp(host='localhost', port=5763):
    connection_string = f'tcp:{host}:{port}'
    print(f"Connecting to {connection_string}...")
    master = mavutil.mavlink_connection(connection_string)
    master.wait_heartbeat()
    print(f"✓ Heartbeat received!")
    return master

def wait_ack(master, expected_cmd=None, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=1)
        if msg:
            if expected_cmd is not None and msg.command != expected_cmd:
                continue
            result_name = RESULT_MAP.get(msg.result, f'UNKNOWN({msg.result})')
            print(f"  ACK: {result_name} (cmd={msg.command})")
            return msg.result == 0
    print("  ACK: TIMEOUT")
    return False

def arm(master, force=False, value=0):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 
        0,              
        1,              
        0,      
        0, 0, 0, 0, 0
    )
    print(f"arming command sent...")
    return wait_ack(master, expected_cmd=400)

def gps_lock(master, timeout=30):
    print("Waiting for GPS lock...")
    start = time.time()
    while time.time() - start < timeout:
        msg = master.recv_match(type='GPS_RAW_INT', blocking=True, timeout=1)
        if msg and msg.fix_type >= 3:
            print(f"✓ GPS lock acquired (fix_type={msg.fix_type})")
            return True
    print("✗ GPS lock timeout")
    return False

def set_mode(master, mode_name):
    mode_mapping = master.mode_mapping()
    mode_num = mode_mapping.get(mode_name.upper())

    if mode_num is None:
        print(f"Mode '{mode_name}' not available.")
        return False

    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        1,
        mode_num,
        0, 0, 0, 0, 0
    )

    return wait_ack(master, expected_cmd=176)

def land_mode(master):
    print("Switching to LAND mode...")
    return set_mode(master, 'AUTOLAND')


def offset_location(lat, lon, north_m, east_m):
    dlat = north_m / 111111
    dlon = east_m / (111111 * math.cos(math.radians(lat)))
    return lat + dlat, lon + dlon

def get_current_location(master, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=1)
        if msg:
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            alt = msg.relative_alt / 1000.0
            return lat, lon, alt
    return None

def guided_reposition(master, lat, lon, alt):
    master.mav.command_int_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_DO_REPOSITION,
        0,
        0,
        -1,
        0,
        0,
        0,
        int(lat * 1e7),
        int(lon * 1e7),
        alt
    )
    print(f"Reposition command sent → {lat}, {lon}, {alt}")
    return True

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    deltphi = math.radians(lat2 - lat1)
    deltambda = math.radians(lon2 - lon1)

    a = math.sin(deltphi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(deltambda/2)**2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

class PositionController:
    def __init__(self, master):
        self.master = master
        self.current_target = None
        self.busy = False
        self.home_position = None

    def initialize(self):
        pos = get_current_location(self.master)
        if not pos:
            raise Exception("Failed to get initial position.")
        self.current_target = pos
        self.home_position = pos
        print(f" Origin initialized at {self.current_target}")

    def move_relative(self, north_m, east_m):
        if self.busy:
            return False

        self.busy = True

        pos = get_current_location(self.master)
        if not pos:
            self.busy = False
            return False

        lat, lon, alt = pos

        new_lat, new_lon = offset_location(lat, lon, north_m, east_m)

        guided_reposition(self.master, new_lat, new_lon, alt)

        self.wait_until_reached(new_lat, new_lon)

        self.busy = False
        return True

    def wait_until_reached(self, target_lat, target_lon, tolerance=120):
        print("Navigating to target...")
        while True:
            pos = get_current_location(self.master)
            if not pos:
                continue

            lat, lon, _ = pos
            distance = haversine_distance(lat, lon, target_lat, target_lon)

            print(f"Distance: {distance:.1f} m")

            if distance <= tolerance:
                print(" Target reached")
                break

            time.sleep(1)

    def fly_to_home(self):
        if not self.home_position:
            return False

        if self.busy:
            return False

        self.busy = True

        home_lat, home_lon, home_alt = self.home_position
        self.current_target = self.home_position

        guided_reposition(self.master, home_lat, home_lon, home_alt)

        self.wait_until_reached(home_lat, home_lon)

        self.busy = False
        return True
    
    def crash(self):
        pos = get_current_location(self.master)
        if not pos:
            return False

        lat, lon, alt = pos

        target_alt = -20  
        guided_reposition(self.master, lat, lon, target_alt)
        return True
    
    def near_home(self, threshold=50):
        if not self.home_position:
            return False

        pos = get_current_location(self.master)
        if not pos:
            return False

        lat, lon, _ = pos
        home_lat, home_lon, _ = self.home_position

        distance = haversine_distance(lat, lon, home_lat, home_lon)
        return distance <= threshold
    
    def go_north(self, meters):
        return self.move_relative(meters, 0)

    def go_south(self, meters):
        return self.move_relative(-meters, 0)

    def go_east(self, meters):
        return self.move_relative(0, meters)

    def go_west(self, meters):
        return self.move_relative(0, -meters)