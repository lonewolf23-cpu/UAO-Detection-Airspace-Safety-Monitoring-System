from filterpy.kalman import KalmanFilter
import numpy as np


class KalmanTracker:

    def __init__(self):

        self.kf = KalmanFilter(dim_x=4, dim_z=2)

        self.kf.x = np.array([0., 0., 0., 0.])

        self.kf.F = np.array([
            [1,0,1,0],
            [0,1,0,1],
            [0,0,1,0],
            [0,0,0,1]
        ])

        self.kf.H = np.array([
            [1,0,0,0],
            [0,1,0,0]
        ])

        self.kf.P *= 1000
        self.kf.R = 5
        self.kf.Q = 0.1


    def predict(self):
        self.kf.predict()
        return self.kf.x


    def update(self, x, y):
        self.kf.update([x,y])
