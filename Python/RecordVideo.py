import cv2
import os
import time

#*'MPEG' -> AVI File Compression
def main():
    file_name = ''.join(filter(str.isalnum, input("Input File Name Here (Omit Extensions) -> ")))
    print("Hit Enter To Start / Stop Recording")
    cam = cv2.VideoCapture(1)

    cwd = os.getcwd()
    print(f"Directory Of File: {cwd}")
    path = cwd + '\\recorded_videos\\' + file_name + '.mp4'
    print(f"Path Of Video File: {path}")

    _, config_frame = cam.read()
    fps = cam.get(cv2.CAP_PROP_FPS)
    video_writer = cv2.VideoWriter(path, 0x7634706d, fps,
                                   (config_frame.shape[1], config_frame.shape[0]))
    recording = False

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
        if recording:
            timer += fTime - iTime
            cv2.putText(display, "Recording In Progress...", (0, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 0), thickness=2)
            video_writer.write(frame)

        cv2.putText(display, str(round(timer, 2)), (550, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), thickness=2)

        cv2.imshow("Pose OpenCV Video Recorder", display)
        iTime = time.time()

    video_writer.release()
    cam.release()


main()
