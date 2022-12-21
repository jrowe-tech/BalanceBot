import cv2
import statistics
from serial_driver import Driver
from threading import Thread
import mediapipe as mp
import os
import pygame
import numpy as np
from time import sleep as s

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

def video2MP(capturePath):
    # Video Capture From CAPTUREPATH
    cap = cv2.VideoCapture(capturePath)

    # Create Loading Template
    template = cv2.imread("pixmaps\\PercentageTemplate.png")

    #Get Frames Per Second
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Setup Configuration Frame
    _, config_frame = cap.read()
    print(config_frame)
    video_writer = cv2.VideoWriter(capturePath.replace(".mp4", "MP.mp4"), 0x7634706d, fps,
                                   (config_frame.shape[1], config_frame.shape[0]))

    # Reset Active Frame To 0 And Reset Frame Counter
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_counter = 0
    frame_cap = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Setup Pose Detection:
    # Static Image -> False
    # Model Complexity -> 0-2, Least To Most Accurate (and slow)
    # Enable Segmentation -> Improves Accuracy and Smoothes Location (recommended)
    with mp_pose.Pose(static_image_mode=False,
                      model_complexity=2,
                      enable_segmentation=True,
                      min_detection_confidence=0.6,
                      min_tracking_confidence=0.6) as pose:
        while True:
            # Count Frames
            frame_counter += 1

            # Read From Video
            active, frame = cap.read()

            if active:

                # print(f"Processing Frame {frame_counter} of {frame_cap}")

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

                # Display Widget
                display = template.copy()
                display = cv2.putText(display, str(frame_counter),
                                      (225, 190), cv2.FONT_HERSHEY_SIMPLEX,
                                      2, (255, 255, 255), 2, cv2.LINE_AA)
                display = cv2.putText(display, str(frame_cap),
                                      (425, 190), cv2.FONT_HERSHEY_SIMPLEX,
                                      2, (255, 255, 255), 2, cv2.LINE_AA)
                display = cv2.putText(display, f"{frame_counter * 100 / frame_cap:.2f}",
                                      (260, 270), cv2.FONT_HERSHEY_SIMPLEX,
                                      1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('Display', display)

                _ = cv2.waitKey(1)


    # Release Video Writer For Low Latency
    video_writer.release()
    cap.release()

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
        self.switch = 'N'

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
                self.currentSteps = self.decompileBytesLeft(self.data[1:4])
                self.switchStates = chr(self.data[0])
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


def arduinoStream(path, frameWidth, frameHeight):
    # For webcam input:
    cap = cv2.VideoCapture(0)

    # Reset Frames
    cv2.destroyAllWindows()

    width = 1280
    height = 720

    # Create / Use Configuration Frame
    _, config_frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    video_writer = cv2.VideoWriter(path, 0x7634706d, fps,
                                   (config_frame.shape[1], config_frame.shape[0]))


    # Call Custom Arduino Pipeline
    # pipe = Pipe()

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

            poseImage = image.copy()
            image.flags.writeable = False

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            poseImage.flags.writeable = False
            poseImage = cv2.cvtColor(poseImage, cv2.COLOR_BGR2RGB)
            results = pose.process(poseImage)

            # Draw the pose annotation on the image.
            poseImage.flags.writeable = True
            poseImage = cv2.cvtColor(poseImage, cv2.COLOR_RGB2BGR)

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

                poseImage = cv2.resize(poseImage, (width, height))

                cv2.ellipse(poseImage, (ShAvgx, ShAvgy), (4, 4), 0, 0, 360, (0, 255, 0), 4)

                midpoint = 640
                min_speed = 10
                distance_from_center = (abs(ShAvgx - 640)) / 180
                distance_from_center = distance_from_center * (180 / 640)
                motor_speed = round(max_motor_speed * distance_from_center)

                num_steps = round(motor_speed / 10)

                if motor_speed < min_speed:
                    num_steps = 0

                # pipe.steps = num_steps
                # pipe.speed = motor_speed

                if ShAvgx > 640:
                    num_steps = 1 * num_steps
                    # pipe.polarity = 0
                    direction = "<-----"

                    if Limit_1 > 0:
                        motor_speed = 0
                        num_steps = 0

                else:
                    # pipe.polarity = 1
                    direction = "----->"

                    if Limit_2 > 0:
                        motor_speed = 0
                        num_steps = 0

                print("MOTOR SPEED: ", motor_speed)
                print("STEPS: ", num_steps)
                print("DIRECTION: " + direction)

            else:
                pass
                # pipe.speed = 0
                # pipe.steps = 0

            poseImage = cv2.flip(poseImage, 1)

            # Flip the image horizontally for a selfie-view display.
            poseImage = cv2.resize(poseImage, (frameWidth, frameHeight))
            cv2.imshow('Display', poseImage)
            frameCount = frameCount + 1

            # Write The Current Frame
            video_writer.write(image)

            if cv2.waitKey(1) & 0xFF in (27, 13):
                # pipe.speed = 0
                # pipe.steps = 0
                # pipe.port.closePort()
                break

        # Release Streaming Agents
        video_writer.release()
        cap.release()

def videoPlayback(basePath, width, height):
    # Create Video Capture Objects
    cap1 = cv2.VideoCapture(basePath)
    cap2 = cv2.VideoCapture(basePath.replace(".mp4", "MP.mp4"))

    # Setup Configuration Frame
    _, config_frame = cap2.read()
    fps = cap2.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")

    # Reset Video
    cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Configure Local Variables
    playing = False
    frame_counter = 0
    frame_cap = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total Frames: {frame_cap}\n"
          f"Total Seconds: {frame_cap / fps:.2f}")
    ui_color = (10, 10, 10)
    frame = None
    display = cv2.imread("pixmaps\\BlankTemplate.png")

    # Set Initial Playing Video
    currentVideo = cap1

    # Create Playback Loop
    while True:
        if playing:
            active, frame = currentVideo.read()

            if active:
                # Frame Counter
                frame_counter += 1

                # Grab Frame For Display
                display = frame.copy()

                # Write Pause Button Onto Widget

                # Declare End Of Video
                if frame_counter == frame_cap:
                    playing = False
            s(1 / fps)

        else:
            if frame is not None:
                display = frame.copy()



        # Get Keybinds For Control Scheme -> Might Switch To Hashmap For Optimization
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key in {13, 32}:
            if (frame_counter == frame_cap):
                frame_counter = 0
                currentVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)
                playing = True
            else:
                playing = not playing
        elif key == 114:
            frame_counter = 0
            currentVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)
            playing = True
        elif key == 111 and frame_counter > 0:
            if currentVideo == cap1:
                currentVideo = cap2
            else:
                currentVideo = cap1
            currentVideo.set(cv2.CAP_PROP_POS_FRAMES, frame_counter - 1)
            active, frame = currentVideo.read()
        elif not playing:
            if key == 97 and frame_counter > 1:
                currentVideo.set(cv2.CAP_PROP_POS_FRAMES, frame_counter - 2)
                active, frame = currentVideo.read()
                frame_counter -= 1

            if key == 100 and frame_counter < frame_cap - 1:
                active, frame = currentVideo.read()
                frame_counter += 1


        # Augment Final Display Frame
        display = cv2.resize(display, (width, height))
        display = cv2.line(display, (0, height-45), (width, height-45), ui_color, 2)
        display = cv2.line(display, (45, height), (45, height-45), ui_color, 2)
        display = cv2.line(display, (60, height-20), (width-15, height-20), (0, 0, 0), 7)
        lineWidth = int(((frame_counter+1) / (frame_cap+1)) * (width-75)) + 60
        display = cv2.line(display, (60, height-20), (lineWidth, height-20), (0, 0, 255), 7)

        if playing:
            display = cv2.line(display, (15, height-10), (15, height-30), (255, 255, 255), 2)
            display = cv2.line(display, (30, height-10), (30, height-30), (255, 255, 255), 2)
        else:
            cv2.fillPoly(display, pts=[np.array([[15, height-10], [15, height-30], [30, height-20]])],
                         color=(255, 255, 255))

        # Show Final Display Frame
        cv2.imshow('Display', display)



    # Reset Video Captures And Stop Function
    cap1.release()
    cap2.release()




def main(displaySize=(640, 360)):
    pygame.init()

    fileName = str(input("Insert Recorded File Directory >>> "))
    if '.mp4' not in fileName:
        fileName += ".mp4"

    # Beep and Boop
    beep = pygame.mixer.Sound('sounds\\beep.wav')
    boop = pygame.mixer.Sound('sounds\\boop.wav')

    # Setup UI To Begin
    cv2.imshow('Display', cv2.imread('pixmaps\\MidtermOpening.png'))
    cv2.waitKey(0)

    # Play Funny Countdown
    cv2.imshow('Display', cv2.imread('pixmaps\\Slide3.png'))
    _ = cv2.waitKey(1)
    beep.play()
    s(1)

    cv2.imshow('Display', cv2.imread('pixmaps\\Slide2.png'))
    _ = cv2.waitKey(1)
    beep.play()
    s(1)

    cv2.imshow('Display', cv2.imread('pixmaps\\Slide1.png'))
    _ = cv2.waitKey(1)
    beep.play()
    s(1)

    # Boop
    boop.play()

    # Record The Video
    arduinoStream(fileName, displaySize[0], displaySize[1])

    # Process The Video
    video2MP(fileName)

    # Create OpenCV Videoplayer Widget
    videoPlayback(fileName, displaySize[0], displaySize[1])

    # Create Final Frame
    cv2.imshow('Display', cv2.imread('pixmaps\\FinalSlide.png'))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main(displaySize=(800, 600))