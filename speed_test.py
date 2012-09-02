import random

from PanTiltSwivel import PanTiltSwivel

def speed_test(sleep, serial_port = None):
    """Allows doing physical speed performance tests by sending random data"""
    pan_tilt_swivel = PanTiltSwivel(serial_port)
    pan_tilt_swivel.set_timeout(sleep)
    while(1):
        pan_tilt_swivel.pan(random.randrange(0, 179, 1))
        pan_tilt_swivel.tilt(random.randrange(0, 179, 1))


if __name__ == "__main__":
    import sys
    serial_port = sys.argv[2] if len(sys.argv) == 3 else None
    speed_test(float(sys.argv[1]), serial_port)
