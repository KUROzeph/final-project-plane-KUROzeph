
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

def go_north(master, meters):
    pos = get_current_location(master)
    if not pos:
        return False
    lat, lon, alt = pos
    new_lat, new_lon = offset_location(lat, lon, meters, 0)
    return guided_reposition(master, new_lat, new_lon, alt)


def go_south(master, meters):
    pos = get_current_location(master)
    if not pos:
        return False
    lat, lon, alt = pos
    new_lat, new_lon = offset_location(lat, lon, -meters, 0)
    return guided_reposition(master, new_lat, new_lon, alt)


def go_east(master, meters):
    pos = get_current_location(master)
    if not pos:
        return False
    lat, lon, alt = pos
    new_lat, new_lon = offset_location(lat, lon, 0, meters)
    return guided_reposition(master, new_lat, new_lon, alt)


def go_west(master, meters):
    pos = get_current_location(master)
    if not pos:
        return False
    lat, lon, alt = pos
    new_lat, new_lon = offset_location(lat, lon, 0, -meters)
    return guided_reposition(master, new_lat, new_lon, alt)






if __name__ == '__main__':
    master = connect_tcp(host='localhost', port=5763)

    gps_lock(master)
    arm(master)

    set_mode(master, 'AUTO')
    print("Taking off...")
    time.sleep(25)    

    set_mode(master, 'GUIDED')
    time.sleep(3)

    go_north(master, 450)
    time.sleep(25)

    go_east(master, 450)
    time.sleep(25)

    go_south(master, 450)
    time.sleep(25)

    go_west(master, 450)
    time.sleep(25)
    