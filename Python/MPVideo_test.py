import cv2
import numpy as np

defaultPaths = ("recorded_videos\\debugVideo.mp4", "recorded_videos\\debugVideoMP.mp4")

default = input("Would You Like To Use Preloaded Videos (y/n) >>> ").lower()

if default == "y":
    path1 = defaultPaths[0]
    path2 = defaultPaths[1]
else:
    print("Test factors of both video files and assert similarity")
    path1 = input("Input File Path (ext/cwd included) >>> ")
    path2 = input("Input File Path (ext/cwd included) >>> ")

vid1 = cv2.VideoCapture(path1)
vid2 = cv2.VideoCapture(path2)

count1 = int(vid1.get(cv2.CAP_PROP_FRAME_COUNT))
count2 = int(vid2.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Video 1 Frame Count: {count1}" f"\nVideo 2 Frame Count: {count2}" \
      f"\nFrame Counts Equal? {count1==count2}")
try:
    input("Hit Enter To Show First Frame Of Each Video")
    _, left = vid1.read()
    print(f"Left Frame Data: {left}")
    left = cv2.resize(left, (1000, 800))
    _, right = vid2.read()
    print(f" Right Frame Data: {right}")
    right = cv2.resize(right, (1000, 800))
    frame = np.hstack((left, right))
    cv2.imshow("Diagnostic Frame", frame)
    print("Hit Enter On Frame To Show Final Frame Of Each Video")
    cv2.waitKey(1)

    print("Hit Enter On Frame To Close Diagnostic")
    vid1.set(cv2.CAP_PROP_POS_FRAMES, count1)
    vid2.set(cv2.CAP_PROP_POS_FRAMES, count2)

    frame = np.hstack((vid1.read(), vid2.read()))
    cv2.imshow("Diagnostic Frame", frame)
    cv2.waitKey(1)
except Exception as e:
    print("Video Reading Failed! Check Inputted Paths Are Correct!")
    print(f"Error: {e}")
else:
    print("Video Reading Successful!")
finally:
    cv2.destroyAllWindows()
    vid1.release()
    vid2.release()