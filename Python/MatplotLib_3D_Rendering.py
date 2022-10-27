import matplotlib.pyplot as plt
import numpy as np
import random
import time
from pose_utils import PoseDetection
import cv2

class PoseRenderer(PoseDetection):
    def __init__(self):
        super().__init__()
        self.mesh_3d = None
        self.figure = plt.figure()
        self.plot = plt.axes(projection='3d')
        self.posePoints3D = None
        self.poseMesh3D = None

    def realtime_detection_3d(self, cid=0):
        cam = cv2.VideoCapture(cid)
        frame_count = 0
        timeI = time.time()
        self.plot.set_zlim(-1, 1)
        self.plot.set_xlim(-1, 1)
        self.plot.set_ylim(-1, 1)
        while True:
            frame_count+=1
            _, frame = cam.read()
            self.plot.set_zlim(-1, 1)
            self.plot.set_xlim(-1, 1)
            self.plot.set_ylim(-1, 1)
            points, connections = self.pose_detection_3d(frame)
            if points:
                self.Create3DMesh(points, connections)
                print(f"Completed: {frame_count}")
                plt.pause(0.001)
        timeF = time.time()
        return timeF - timeI



    def Create3DMesh(self, points, connections):

        if self.posePoints3D is not None:
            plt.cla()

        #Compile List Of Mesh Points
        all_points = points.values()
        xPoints = [point[0] for point in all_points]
        yPoints = [point[1] for point in all_points]
        zPoints = [point[2] for point in all_points]

        #Plot 3D Points
        self.plot.set_zlim(-0.4, 0.4)
        self.plot.set_xlim(-0.4, 0.4)
        self.plot.set_ylim(-0.4, 0.4)
        self.posePoints3D = self.plot.scatter3D(xPoints, yPoints, zPoints, c=zPoints, cmap='hsv')

        for segment in connections:
            #Create Line With 100 Segmentations -> Cut Down For Optimizations
            xLine = np.linspace(points[segment[0]][0], points[segment[1]][0], 100)
            yLine = np.linspace(points[segment[0]][1], points[segment[1]][1], 100)
            zLine = np.linspace(points[segment[0]][2], points[segment[1]][2], 100)

            #Create Line Plot
            self.poseMesh3D = self.plot.plot3D(xLine, yLine, zLine, 'red')


def animated_plots():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Make the X, Y meshgrid.
    xs = np.linspace(-1, 1, 50)
    ys = np.linspace(-1, 1, 50)
    X, Y = np.meshgrid(xs, ys)

    # Set the z axis limits so they aren't recalculated each frame.
    ax.set_zlim(-1, 1)

    # Begin plotting.
    wframe = None
    tstart = time.time()
    for phi in np.linspace(0, 180. / np.pi, 100):
        # If a line collection is already remove it before drawing.
        if wframe:
            wframe.remove()
        # Generate data.
        Z = 0.2*np.cos(3 * np.pi * X + phi) + 0.1*np.sin(2 * np.pi * Y + phi)#* (1 - np.hypot(X, Y))
        print(type(Z))
        # Plot the new wireframe and pause briefly before continuing.
        wframe = ax.plot_wireframe(X, Y, Z, rstride=5, cstride=1)
        plt.pause(.1)

    print('Average FPS: %f' % (100 / (time.time() - tstart)))


#Create3DMesh({"head":np.array([1, 20, 0.2]),
#                   "leg":np.array([0, 0, 0])},
#                  [("head", "leg")])
#animated_plots()
def timeFunction(function):
    timeI = time.time()
    function.realtime_detection_3d(0)
    timeF = time.time()
    return timeF - timeI

def practice_function():
    time.sleep(10)

renderer = PoseRenderer()
print(renderer.realtime_detection_3d(0))
