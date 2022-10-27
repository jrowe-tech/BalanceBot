import cv2
import mediapipe as mp
import numpy as np
import os
import time
from threading import Thread

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name

def static_mediapipe_3d(img):
    return


def mediapipe_2d(img):
    # For static images:

    pose = mp_pose.Pose(static_image_mode=True, model_complexity=2,
            enable_segmentation=True, min_detection_confidence=0.5)

    image_height, image_width, _ = img.shape

    # Convert the BGR image to RGB before processing.

    results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        img,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style())

    # Plot pose world landmarks.
    # mp_drawing.plot_landmarks(
    #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    return img


def ModifyVideo(path, viewport="2d"):
    try:
        cap = cv2.VideoCapture(path)

        frame_counter = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Frames: {total_frames}")

        ###Add Additional Demoing Functions Right HERE (: ----->
        viewport_2d_functions = [mediapipe_2d]
        viewport_3d_functions = [mediapipe_3d]

        #Set Cached Video Path -> Default is .cache
        PATH = os.getcwd() + "\\.cache\\"

        #Read initial video frame for image configuration
        _, config_frame = cap.read()
        vsets = {"fourcc":0x7634706d, "fps":30.0,
                 "width":config_frame.shape[1], "height":config_frame.shape[0]}

        #RESET Video
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if viewport == "3d":
            modified_videos = [cv2.VideoWriter(PATH + function.__name__ + '.mp4', vsets['fourcc'],
                                vsets['fps'], (vsets['width'], vsets['height']))
                               for function in viewport_3d_functions]
        else:
            modified_videos = [cv2.VideoWriter(PATH + function.__name__ + '.mp4', vsets['fourcc'],
                                vsets['fps'], (vsets['width'], vsets['height']))
                               for function in viewport_2d_functions]

        # Read until video is completed
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:

                #Track Frames And Print
                frame_counter += 1
                print(f"Frame {frame_counter} Of {total_frames}")

                #Necessary WaitKey For God Knows What Reason
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

                #Break On Complete Capture
                #if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    #break

                #Apply Video Functions And Write To Video Writers
                if viewport == "3d":
                    for i in range(len(viewport_3d_functions)):
                        modified_videos[i].write(viewport_3d_functions[i](frame))
                else:
                    for i in range(len(viewport_2d_functions)):
                        modified_videos[i].write(viewport_2d_functions[i](frame))

            # Video Doesn't Exist Or Frame Read Broke
            else:
                return "FrameReadError"

        for i in range(len(modified_videos)):
            modified_videos[i].release()

        cap.release()
        return
    except Exception as e:
        return e


#Mediapipe With Local Loop (For Threading)
def static_mediapipe_2d(capturePath, savePath):
    #Video Capture From CAPTUREPATH
    cap =  cv2.VideoCapture(capturePath)

    #Setup Configuration Frame
    _, config_frame = cap.read()
    video_writer = cv2.VideoWriter(".cache\\" + savePath, 0x7634706d, 30.0,
                                   (config_frame.shape[1], config_frame.shape[0]))

    #Reset Active Frame To 0 And Reset Frame Counter
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_counter = 0

    #Setup Pose Detection:
    #Static Image -> False
    #Model Complexity -> 0-2, Least To Most Accurate (and slow)
    #Enable Segmentation -> Improves Accuracy and Smoothes Location (recommended)
    with mp_pose.Pose(static_image_mode=False,
                      model_complexity=2,
                      enable_segmentation=True,
                      min_detection_confidence=0.8,
                      min_tracking_confidence=0.8) as pose:
        while True:
            #Count Frames
            frame_counter += 1

            #Read From Video
            active, frame = cap.read()

            if active:
                #Mediapipe Processing
                results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style())

                #Break When Video Ends
                if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    break

                #Write To Save Path
                video_writer.write(frame)

    #Release Video Writer For Low Latency
    video_writer.release()



#result = ModifyVideo("recorded_videos/demo.mp4")

#result = static_mediapipe_2d("recorded_videos/demo.mp4")


#Create Threads For Each Function And Run
def thread_packages(path, viewport="2d"):
    #Setup Recorded Path
    RECORDED_PATH = "recorded_videos\\" + path

    try:
        #Define Pose Functions
        pose_functions_2d = [static_mediapipe_2d]
        pose_functions_3d = []

        #Create Threads For Each Active Function
        if viewport == "3d":
            threads = [Thread(target=function, args=(RECORDED_PATH, function.__name__ + ".mp4"))
                       for function in pose_functions_3d]
        else:
            threads = [Thread(target=function, args=(RECORDED_PATH, function.__name__ + ".mp4"))
                       for function in pose_functions_2d]

        #Start Threads
        for thread in threads:
            thread.start()

        #Combine Threads
        for thread in threads:
            thread.join()

    #Print Whatever Went Wrong
    except Exception as e:
        print(f"Failed: {e}")


#Run Threading Function And Count Time
def main():
    #Start Timer
    start_time = time.perf_counter()

    #Thread Each Package With File Path and Viewport Type
    thread_packages("FPSCheck.mp4", "2d")

    #Stop Timer
    stop_time = time.perf_counter()

    #Print Time Of Threading Completion
    print(f"Time Of Completion {round(stop_time - start_time, 3)}")


#Define Main
main()