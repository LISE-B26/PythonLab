# B26 Lab Code
# Last Update: 2/3/15

import serial

# Translations of the controller's status messages
MEASUREMENT_STATUS = {
    '0': 'Measurement data okay',
    '1': 'Underrange',
    '2': 'Overrange',
    '3': 'Sensor error',
    '4': 'Sensor off',
    '5': 'No sensor',
    '6': 'Identification error',
    '7': 'Error FRG-720, FRG-730'
}

# Translation of the controller's units check  messages
MEASUREMENT_UNITS = {
    '0': 'mbar/bar',
    '1': 'Torr',
    '2': 'Pascal',
    '3': 'Micron'
}

# ASCII Characters used for controller communication
ETX = chr(3)  # \x03
CR = chr(13)
LF = chr(10)
ENQ = chr(5)  # \x05
ACK = chr(6)  # \x06
NAK = chr(21)  # \x15

class AGC100:

    def __init__(self, port = 8, timeout = 1):
        # The serial connection should be setup with the following parameters:
        # 1 start bit, 8 data bits, No parity bit, 1 stop bit, no hardware
        # handshake. These are all default for Serial and therefore not input
        # below
        self.ser = serial.Serial(port = port, timeout = timeout)

    def checkAcknowledgement(self, response):
        if (response == NAK + CR + LF):
            message = 'Serial communication returned negative acknowledge (NAK). ' \
                      'Check AGC100 documentation for more details.'
            raise IOError(message)
        elif (response != ACK + CR + LF):
            message = 'Serial communication returned unknown response:\n{}' \
                ''.format(repr(response))
            raise IOError(message)

    def getPressure(self):
        assert self.ser.isOpen()

        self.ser.write('PR1' + CR + LF)
        acknowledgement = self.ser.readline()
        self.checkAcknowledgement(acknowledgement)

        self.ser.write(ENQ)
        errMsgAndPressure = self.ser.readline().rstrip(LF).rstrip(CR)

        errMsg = errMsgAndPressure[0]
        pressure = errMsgAndPressure[3:]

        if errMsg != '0':
            message = 'Pressure query resulted in an error: ' + MEASUREMENT_STATUS[errMsg]
            raise IOError(message)

        self.ser.write(CR + LF)
        return pressure

    def getGaugeModel(self):
        assert self.ser.isOpen()

        self.ser.write('TID' + CR + LF)
        acknowledgement = self.ser.readline(25)
        self.checkAcknowledgement(acknowledgement)

        self.ser.write(ENQ)
        model = self.ser.readline().rstrip(LF).rstrip(CR)

        self.ser.write(CR + LF)

        return model

    def getUnits(self):
        assert self.ser.isOpen()

        self.ser.write('UNI' + CR + LF)
        acknowledgement = self.ser.readline()
        self.checkAcknowledgement(acknowledgement)

        self.ser.write(ENQ)
        unit = MEASUREMENT_UNITS[self.ser.readline().rstrip(LF).rstrip(CR)]

        self.ser.write(CR + LF)

        return unit

    def closeConnection(self):
        self.ser.close()


if __name__ == '__main__':

    controller = AGC100()
    print 'The gauge model number is ' + controller.getGaugeModel()
    print 'The current pressure is ' + controller.getPressure() + ' ' + controller.getUnits()

    controller.closeConnection()