import serial.tools.list_ports_windows as ports
import serial

class Driver:
    def __init__(self, baud, buffer):
        self.comports = []
        print("\nOPEN COMPORTS:")
        for port in ports.comports():
            self.comports.append(str(port)[:4])
            print(port)

        self.portID = "COM" + input("\nCHOOSE A PORT: COM")
        if self.portID not in self.comports:
            raise AttributeError

        self.serial = serial.Serial(timeout=0.0001)
        self.serial.baudrate = baud
        self.serial.port = self.portID
        self.serial.open()
        self.bufferSize = buffer
        self.buffer = 0
        self.maxReadLength = 5

    def sendValue(self, data):
        self.serial.write(data)
        if self.buffer >= self.bufferSize:
            self.serial.flush()
            self.buffer = 0
        self.buffer += 1

    def readValue(self):
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.flush()
        return self.serial.read()

    def readLine(self):
        data = self.serial.readline()
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.flush()
        return [byte for byte in data if len(data) <= 4 and
                data is not None]

    def startSend(self):
        self.serial.write(0xCC)

    def closePort(self):
        self.serial.flush()
        self.serial.cancel_read()
        self.serial.cancel_write()
        self.serial.close()

