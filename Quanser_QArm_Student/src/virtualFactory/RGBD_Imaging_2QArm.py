# Note use this method to get your qvl libraries to ensure you're using the
# latest version in GitHub. It is inserted first in the list to take precedence
# over all other libraries in your python path.
import sys
sys.path.insert(0, "../")

from qvl.qlabs import QuanserInteractiveLabs
from qvl.conveyor_curved import QLabsConveyorCurved
from qvl.conveyor_straight import QLabsConveyorStraight
from qvl.widget import QLabsWidget
from qvl.delivery_tube import QLabsDeliveryTube
from qvl.basic_shape import QLabsBasicShape
from qvl.generic_sensor import QLabsGenericSensor
from qvl.qarm import QLabsQArm
from qvl.real_time import QLabsRealTime
import pal.resources.rtmodels as rtmodels
from pal.products.qarm import QArm, QArmRealSense
import time
import math
import struct
import numpy as np
import cv2
import os
from random import randrange

######### Main setup script ##########

## CHANGE THE DIRECTORY IF WE ARE GOING TO MAKE THESE PUBLIC

__qalDirPath = os.environ['RTMODELS_DIR']

QARMS = os.path.normpath(
    os.path.join(__qalDirPath, 'QArms'))


# Core variables
waitTime = 1.0

qlabs = QuanserInteractiveLabs()
print("Connecting to QLabs...")
try:
    qlabs.open("localhost")
except:
    print("Unable to connect to QLabs")

print("Connected")

qlabs.destroy_all_spawned_actors()
QLabsRealTime().terminate_all_real_time_models()

time.sleep(1)


#region : create arms and supports
# ########## Create an arm ##########
firstArm = QLabsQArm(qlabs)
firstArm.spawn_id_degrees(actorNumber = 10,
                            location = [1, -0.5, 0.3],
                            rotation = [0, 0, 0],
                            scale = [1, 1, 1],
                            configuration = 0,
                            waitForConfirmation = True)

# Create a simple support for the arm
firstArmStand = QLabsBasicShape(qlabs)
firstArmStand.spawn_id_and_parent_with_relative_transform(actorNumber = 100,
                                                            location = [0, 0, -0.15],
                                                            rotation = [0, 0, 0],
                                                            scale = [0.3, 0.3, 0.3],
                                                            configuration = 0,
                                                            parentClassID = firstArm.classID,
                                                            parentActorNumber = 10,
                                                            parentComponent = 0,
                                                            waitForConfirmation = True)
firstArmStand.set_material_properties(color = [0.3, 0.3, 0.3],
                                        roughness = 0.4, metallic = False)

secondArm = QLabsQArm(qlabs)
secondArm.spawn_id_degrees(actorNumber = 11,
                            location = [0, -0.5, 0.3],
                            rotation = [0, 0, 0],
                            scale = [1, 1, 1],
                            configuration = 0,
                            waitForConfirmation = True)

# Create a simple support for the arm
secondArmStand = QLabsBasicShape(qlabs)
secondArmStand.spawn_id_and_parent_with_relative_transform(actorNumber = 101,
                                                            location = [0, 0, -0.15],
                                                            rotation = [0, 0, 0],
                                                            scale = [0.3, 0.3, 0.3],
                                                            configuration = 0,
                                                            parentClassID = secondArm.classID,
                                                            parentActorNumber = 11,
                                                            parentComponent = 0,
                                                            waitForConfirmation = True)
secondArmStand.set_material_properties(color = [0.3, 0.3, 0.3],
                                        roughness = 0.4, metallic = False)

#endregion

cylinder = QLabsWidget(qlabs)

cylinder.spawn(location = [1, .5, 0],
               rotation = [0, 0, 0],
               scale = [.05, .05, 1],
               configuration = cylinder.CYLINDER,
               color = [0,0,1],
               measuredMass = 1)

cylinder.spawn(location = [0, .5, 0],
               rotation = [0, 0, 0],
               scale = [.05, .05, 1],
               configuration = cylinder.CYLINDER,
               color = [0,1,0],
               measuredMass = 1)


# # Start spawn model
QLabsRealTime().start_real_time_model(QARMS+'/QArm_Spawn0', actorNumber=10, additionalArguments='-uri_hil tcpip://localhost:18900 -uri_video tcpip://localhost:18901')
QLabsRealTime().start_real_time_model(QARMS+'/QArm_Spawn1', actorNumber=11, additionalArguments= '-uri_hil tcpip://localhost:18902 -uri_video tcpip://localhost:18903')

#Initial Setup
runTime = 30.0 # seconds
max_distance = 2 # meters (for depth camera)

with QArmRealSense(hardware=0, videoPortNumber=18901) as myCam1, QArmRealSense(hardware=0, videoPortNumber=18903) as myCam2:
    t0 = time.time()
    while time.time() - t0 < runTime:

        myCam1.read_RGB()
        cv2.imshow('My RGB', myCam1.imageBufferRGB)

        myCam1.read_depth()
        cv2.imshow('My Depth', myCam1.imageBufferDepthPX/max_distance)

        myCam2.read_RGB()
        cv2.imshow('My RGB2', myCam2.imageBufferRGB)

        myCam2.read_depth()
        cv2.imshow('My Depth2', myCam2.imageBufferDepthPX/max_distance)

        cv2.waitKey(1)



# ## ONE ARM ///////////////////////////////////////////

# #Initial Setup
# runTime = 30.0 # seconds
# max_distance = 1 # meters (for depth camera)

# with QArmRealSense(hardware=0) as myCam1:
#     t0 = time.time()
#     while time.time() - t0 < runTime:

#         myCam1.read_RGB()
#         cv2.imshow('My RGB', myCam1.imageBufferRGB)

#         myCam1.read_depth()
#         cv2.imshow('My Depth', myCam1.imageBufferDepthPX/max_distance)

#         cv2.waitKey(10)