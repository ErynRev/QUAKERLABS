from pal.products.qarm import QArm, QArmRealSense
from hal.products.qarm import QArmUtilities
import time
import numpy as np


def createQarm(hilPortNumber = 18900):
    # Load QArm in Position Mode
    myArm = QArm(hardware=0, hilPortNumber= hilPortNumber)
    return myArm

def createQarmCamera(videoPortNumber = 18901):
    # Load QArm in Position Mode
    myArm = QArmRealSense(hardware=0, videoPortNumber= videoPortNumber)
    return myArm

def pickAndPlace(myArm, state):

    #region: Setup
    # Timing Parameters and methods
    startTime = time.time()
    def elapsed_time():
        return time.time() - startTime

    # Load QArm in Position Mode
    myArmUtilities = QArmUtilities()

    # Reset startTime before Main Loop
    startTime = time.time()
    #endregion

    closed = .85

    #region: Main Loop

    positions = [[.27, 0, .23, 0],[0.53,-.025,.13,0],[0.53,-.025,.13,closed],
                 [.3, -.2, .3, closed], [0, -.4, .1, closed],
                 [0, -.4, .1, 0], [.27, 0, .23, 0]]

    ledCmd = np.array([0, 1, 1], dtype=np.float64)
    currentPosition = positions[state]

    positionCmd = currentPosition[0:3]
    gripCmd = currentPosition[3]

    allPhi, phiCmd = myArmUtilities.qarm_inverse_kinematics(positionCmd, 0, myArm.measJointPosition[0:4])

    myArm.read_write_std(phiCMD=phiCmd, grpCMD=gripCmd, baseLED=ledCmd)

def terminate(myArm):
    myArm.terminate()



