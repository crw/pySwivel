import time
import glob
import logging

import serial


class CommandError(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Invalid command: " + data


class PanTiltSwivel:

    __RXTX_SLEEP_TIME = 0.05
    __COMMAND_LENGTH_BYTES = 2
    __SERVO_MIN_TRAVEL = 0
    __SERVO_MAX_TRAVEL = 179
    __CMD_START = chr(0x00)
    __CMD_PAN = 'p'
    __CMD_TILT = 't'


    def __init__(self, serial_port = None):
        """serial is a valid serial port"""
        if serial_port is None:
            serial_port = PanTiltSwivel.get_default_serial_port()
        self.serial = serial.Serial(serial_port, 9600)

    @classmethod
    def get_default_serial_port(cls):
        return glob.glob('/dev/tty.usbmodem*')[0]


    def set_timeout(self, sleep_ms):
        """Sets the RXTX cool-down timeout"""
        self.__RXTX_SLEEP_TIME = sleep_ms


    def __serialTX(self, data):
        """Writes data out to the arduino interface

        TODO: Should be refactored into an ArduinoSerial class
        """
        b = self.serial.write(data)
        logging.info("Message: ", data, ",", b, "bytes.")
        time.sleep(self.__RXTX_SLEEP_TIME)


    def __send_command(self, command, data):
        """Formats command for the arduino interface

        TODO: Should be refactored into an ArduinoSerial class
        """
        if len(command+data) is self.__COMMAND_LENGTH_BYTES:
            self.__serialTX(self.__CMD_START+command+data)
        else:
            raise CommandError(command+data)


    def __valid_angle(self, angle):
        """Validates angle is within servo specification"""
        if (angle >= self.__SERVO_MIN_TRAVEL and
            angle <= self.__SERVO_MAX_TRAVEL):
            return True
        else:
            logging.warning("Requested angle out of bounds: " + str(angle))
            return False


    def __angle_to_value(self, angle):
        """Formats angle data for the arduino interface

        TODO: Should be refactored into an ArduinoSerial class
        """     
        return chr(angle)


    def __send_servo_command(self, command, angle):
        """Send a pan or tilt command to the servos"""
        if self.__valid_angle(angle):
            self.__send_command(command, self.__angle_to_value(angle))


    def pan(self, angle):
        """Pan the mount to the specified angle"""
        self.__send_servo_command(self.__CMD_PAN, angle)


    def tilt(self, angle):
        """Tilt the mount to the specified angle"""
        self.__send_servo_command(self.__CMD_TILT, angle)
