from PanTiltSwivel import PanTiltSwivel

if __name__ == "__main__":
    import sys
    serial_port = sys.argv[2] if len(sys.argv) == 3 else None
    pts = PanTiltSwivel(serial_port)
    pts.pan(int(sys.argv[1]))