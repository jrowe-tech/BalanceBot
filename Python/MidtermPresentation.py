import cv2
import statistics
from serial_driver import Driver
from threading import Thread
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

def video2MP(capturePath):
    # Video Capture From CAPTUREPATH
    cap = cv2.VideoCapture("recorded_videos\\" + capturePath)

    #Get Frames Per Second
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Setup Configuration Frame
    _, config_frame = cap.read()
    print(config_frame)
    video_writer = cv2.VideoWriter("recorded_videos\\" + capturePath + "MP.mp4", 0x7634706d, fps,
                                   (config_frame.shape[1], config_frame.shape[0]))

    # Reset Active Frame To 0 And Reset Frame Counter
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_counter = 0
    frame_cap = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Setup Pose Detection:
    # Static Image -> False
    # Model Complexity -> 0-2, Least To Most Accurate (and slow)
    # Enable Segmentation -> Improves Accuracy and Smoothes Location (recommended)
    with mp_pose.Pose(static_image_mode=False,
                      model_complexity=2,
                      enable_segmentation=True,
                      min_detection_confidence=0.8,
                      min_tracking_confidence=0.8) as pose:
        while True:
            # Count Frames
            frame_counter += 1

            # Read From Video
            active, frame = cap.read()

            if active:

                print(f"Processing Frame {frame_counter} of {frame_cap}")

                frame.flags.writeable = False

                # Mediapipe Processing
                results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style())

                # Break When Video Ends
                if frame_counter == frame_cap:
                    break

                # Write To Save Path
                video_writer.write(frame)

    # Release Video Writer For Low Latency
    video_writer.release()

#Directly import PIPE
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


def arduinoStream():
    # For webcam input:
    cap = cv2.VideoCapture(0)
    width = 1280
    height = 720

    # Call Custom Arduino Pipeline
    pipe = Pipe()

    print("Camera Setting Completed")

    frameCount = 0
    Limit_1 = 0
    Limit_2 = 0

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    print("\n Neural Network is Loaded \n")

    max_motor_speed = 100

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            image = cv2.resize(image, (640, 360))

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks is not None:

                Sh1x = results.pose_landmarks.landmark[11].x * width
                Sh2x = results.pose_landmarks.landmark[12].x * width
                Sh1y = results.pose_landmarks.landmark[11].y * height
                Sh2y = results.pose_landmarks.landmark[12].y * height

                # print("\nSHOULDER_1_X: ", Sh1x)
                # print("SHOULDER_1_Y: ", Sh1y)
                # print("\nSHOULDER_2_X: ", Sh2x)
                # print("SHOULDER_2_Y: ", Sh2y)

                ShX_List = [float(Sh1x), float(Sh2x)]
                ShY_List = [float(Sh1y), float(Sh2y)]

                ShAvgx = int(statistics.mean(ShX_List))
                ShAvgy = int(statistics.mean(ShY_List))

                image = cv2.resize(image, (width, height))

                cv2.ellipse(image, (ShAvgx, ShAvgy), (4, 4), 0, 0, 360, (0, 255, 0), 4)

                midpoint = 640
                min_pixels = 10
                distance_from_center = (abs(ShAvgx - 640)) / 180
                distance_from_center = distance_from_center * (180 / 640)
                motor_speed = round(max_motor_speed * distance_from_center)


                num_steps = round(motor_speed / 10)


                pipe.steps = num_steps
                pipe.speed = motor_speed

                if ShAvgx > 640:
                    num_steps = 1 * num_steps
                    pipe.polarity = 0
                    direction = "<-----"

                    if Limit_1 > 0:
                        motor_speed = 0
                        num_steps = 0

                else:
                    pipe.polarity = 1
                    direction = "----->"

                    if Limit_2 > 0:
                        motor_speed = 0
                        num_steps = 0

                print("MOTOR SPEED: ", motor_speed)
                print("STEPS: ", num_steps)
                print("DIRECTION: " + direction)

            else:
                pipe.speed = 0
                pipe.steps = 0

            image = cv2.resize(image, (width, height))

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            frameCount = frameCount + 1

            if cv2.waitKey(5) & 0xFF == 27:
                break

def main():
    fileName = str(input("Insert Recorded File Name"))
    input("Hit Enter To Begin Following")


main()