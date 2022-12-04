import cv2
import os
import time
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles


# *'MPEG' -> AVI File Compression
def main():
    file_name = ''.join(filter(str.isalnum, input("Input File Name Here (Omit Extensions) -> ")))
    print("Hit Enter To Start / Stop Recording")
    cam = cv2.VideoCapture(0)

    cwd = os.getcwd()
    print(f"Directory Of File: {cwd}")
    path = cwd + '\\recorded_videos\\' + file_name + '.mp4'
    print(f"Path Of Video File: {path}")

    _, config_frame = cam.read()
    fps = cam.get(cv2.CAP_PROP_FPS)
    video_writer = cv2.VideoWriter(path, 0x7634706d, fps,
                                   (config_frame.shape[1], config_frame.shape[0]))
    recording = False

    counter = 0
    timer = 0
    iTime = 0
    while cam.isOpened():
        active, frame = cam.read()
        frame.flags.writeable = False
        display = frame.copy()

        if not active:
            print("No Camera Detected!")
            continue

        exit_key = cv2.waitKey(1)
        if exit_key == 27:
            break
        if exit_key == 13:
            recording = not recording

        fTime = time.time()

        cv2.putText(frame, str(counter), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), thickness=2)

        if recording:
            timer += fTime - iTime
            cv2.putText(display, "Recording In Progress...", (0, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 0), thickness=2)
            video_writer.write(frame)

        cv2.putText(display, str(round(timer, 2)), (550, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), thickness=2)

        counter += 1
        cv2.imshow("Pose OpenCV Video Recorder", display)
        iTime = time.time()

    video_writer.release()
    cam.release()
    cv2.destroyAllWindows()
    return path


def video2MP(capturePath, savePath):
    # Video Capture From CAPTUREPATH
    cap = cv2.VideoCapture(capturePath)

    #Get Frames Per Second
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Setup Configuration Frame
    _, config_frame = cap.read()
    print(config_frame)
    video_writer = cv2.VideoWriter("recorded_videos\\" + savePath + ".mp4", 0x7634706d, fps,
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


capturePATH = main()
video2MP(capturePATH, input("New Path HERE >>> "))

