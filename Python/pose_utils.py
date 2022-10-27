import cv2
import mediapipe as mp
import numpy as np
import sys

mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

class PoseDetection:
    def __init__(self):
        self.camera = None
        self.path = None
        self.PATH = "\\.cache\\"
        self.mediapipe_pose_model = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

        #mp_pose.Pose(static_image_mode=False,
        #   model_complexity=0, enable_segmentation=True, min_detection_confidence=0.5)
        self.mp_pose_landmarks = (
        "nose", "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner", "right_eye", "right_eye_outer",
        "left_ear", "right_ear", "mouth_left", "mouth_right", "left_shoulder",
        "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_pinky", "right_pinky",
        "left_index", "right_index", "left_thumb", "right_thumb", "left_hip", "right_hip",
        "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel", "right_heel", "left_foot_index",
        "right_foot_index")
        self.excluded_landmarks = excluded_landmarks = {20, 18, 22, 21, 19, 17, 29, 31, 30, 32}
        self.mp_connections = mp_pose.POSE_CONNECTIONS


    def pose_detection_3d(self, img):
        #Process Image With Current Model
        results = self.mediapipe_pose_model.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Input -> detected_points.landmark -> List Of Landmarks -> Apply Naming Convention (with exclusion list)

        #point_no, point_val = enumerate(results)
        detected_points = results.pose_world_landmarks
        if detected_points is None:
            return None, None

        landmarks = detected_points.landmark
        pointIds = [count for count, value in enumerate(landmarks)
                    if value.visibility > 0.5]

        pointPositions = [np.array([landmarks[id].x, landmarks[id].z, -landmarks[id].y])
                          for id in pointIds]

        markedPoints = dict(zip(pointIds, pointPositions))

        #mp_pose = mp.solutions.pose -> Referenced inside of PoseDetection
        connectedJoints = [connection for connection in self.mp_connections
                           if connection[0] in pointIds and connection[1] in pointIds]

        return markedPoints, connectedJoints

detection = PoseDetection()

out, conns = detection.pose_detection_3d(cv2.imread("recorded_videos\\testImg.jpg"))
print(out)
print(conns)