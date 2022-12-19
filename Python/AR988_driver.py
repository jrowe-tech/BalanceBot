from serial_driver import Driver
from time import sleep as s


from threading import Thread

class Pipe:
    def __init__(self):
        # Set Serial Driver and port data
        self.port = Driver(115200, 200)
        self.data = None
        self.dataCount = 0
        self.switchStates = {"N", "L", "R", "B"}
        self.speed = 60
        self.currentSteps = 0
        self.polarity = 0
        self.steps = 0

        thread = Thread(target=self.writeSerial, daemon=True)
        thread.start()

    def processInt(self, x: int) -> bytes:
        return x.to_bytes(1, "big")

    def compileSpeedByte(self, rSpeed: int, cw: bool):
        speedByte = 0
        if cw:
            speedByte |= 128

        speedByte |= max(min(100, abs(rSpeed)), 0)

        return speedByte

    def writeSerial(self):
        cw = True
        while True:

            # Keep Speed Between 0 - 100 -> 255 Reset Override

            # Recommended: Steps From 20 - 100 -> Don't go above ):
            self.steps = 50

            # Polarity -> Licherally Just Set 0 -> CW 1-> CCW
            polarity = 1

            self.port.sendValue(self.processInt(self.speed))
            self.port.sendValue(self.processInt(self.steps))
            self.port.sendValue(self.processInt(self.polarity))

            self.data = self.port.readLine()

            if len(self.data) == 4 and chr(self.data[0]) in self.switchStates:
                # print(f"Read Data: {self.data}")
                # print(f"Limit Switch State: {chr(self.data[0])}")
                self.currentSteps = self.decompileBytesLeft(self.data[1:4])
                # print(f"Arduino Steps: {currentSteps}")
                self.dataCount += 1

    def decompileBytesLeft(self, data: list) -> int:
        count = 0
        for i in range(len(data)):
            count += data[-(i + 1)] << (8 * i)
        return count

    def inputThread(self):
        while True:
            self.speed = int(input("Add New Speed Here -> (0-99) "))
            self.polarity = int(input("Which Direction (0 / 1) "))
            print(f"Current Step Count: {self.currentSteps}")
