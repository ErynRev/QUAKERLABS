import sys
sys.path.append('C:/Users/lm6g20/Documents/Quanser_QArm_Student/libraries/python')
from qvl.qlabs import QuanserInteractiveLabs
from qvl.system import QLabsSystem
from qvl.free_camera import QLabsFreeCamera
from qvl.basic_shape import QLabsBasicShape
from qvl.qarm import QLabsQArm
from qvl.widget import QLabsWidget
from qvl.real_time import QLabsRealTime
from pal.products.qarm import QArm, QArmRealSense
from pal.utilities.vision import Camera3D
from random import randrange
import os
from pathlib import Path

class QArmWorkspace:

    ''' This QArm workspace class is used to create the work environment for QArm to proceed the pick and drop tasks. 
   There are 4 cells assigned with 3 random colours (red, green, blue) and 2 cell types (D-cell, 18650 cell).'''

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# region: Initialise the work space

    def __init__(self):
        self.qlabs = QuanserInteractiveLabs()
        self.hSystem = None
        self.camera = None
        self.baseTable = None
        self.baseMat = None
        self.QArm = None
        self.redBin = None
        self.greenBin = None
        self.blueBin = None
        self.dCellBin = None
        self.cell18650Bin = None
        self.cellRack = None
        self.cellWidget = None

    def connect_to_qlabs(self):

        ''' Connect to the Qlab virtual environment. '''

        print("Connecting to QLabs...")
        try:
            self.qlabs.open("localhost")
            print("Connected")
        except Exception as e:
            print(f"Unable to connect to QLabs: {e}")

    def initialise_system(self):
        self.hSystem = QLabsSystem(self.qlabs)
        self.hSystem.set_title_string('Your Username') ## CHANGE YOUR USERNAME
        self.qlabs.destroy_all_spawned_actors()
        QLabsRealTime().terminate_all_real_time_models()

# endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# region: Create components

    ##### Create QArm worksapce ######

    def create_workspace(self):

        ''' Create camera, based table, based mat, cell rack, bins and QArm in the workspace. '''

        # Create camera and initialise it
        self.camera = QLabsFreeCamera(self.qlabs)
        self.camera.spawn_id(actorNumber=0,
                             location=[2, 2, 2],
                             rotation=[0, 0.5, -2.3],
                             scale=[1, 1, 1],
                             configuration=0,
                             waitForConfirmation=True)
        self.camera.possess()

        # Create base table
        self.baseTable = QLabsBasicShape(self.qlabs)
        self.baseTable.spawn_id(actorNumber=1,
                                location=[0, 0, 0.35],
                                rotation=[0, 0, 0],
                                scale=[2.5, 2.5, 0.7],
                                configuration=0,
                                waitForConfirmation=True)
        self.baseTable.set_material_properties(color=[0.1, 0.1, 0.1],
                                                roughness=0.4,
                                                metallic=False)

        # Create base mat
        self.baseMat = QLabsBasicShape(self.qlabs)
        self.baseMat.spawn_id(actorNumber=2,
                              location=[0, 0, 0.75],
                              rotation=[0, 0, 0],
                              scale=[2, 2, 0.1],
                              configuration=1,
                              waitForConfirmation=True)
        self.baseMat.set_material_properties(color=[0.3, 0.3, 0.3],
                                              roughness=0.4,
                                              metallic=False)
        self.baseMat.set_enable_collisions(enableCollisions=True,
                                            waitForConfirmation=True)
        
        # Create one QArm
        self.QArm = QLabsQArm(self.qlabs)
        self.QArm.spawn_id_degrees(actorNumber=3,
                                   location=[0, 0, 0.8],
                                   rotation=[0, 0, -90],
                                   scale=[1, 1, 1],
                                   configuration=0,
                                   waitForConfirmation=True)

        # Create bins
        # Create red D-cell bin
        self.redDcellBin = QLabsBasicShape(self.qlabs)
        self.redDcellBin.spawn_id_box_walls_from_center_degrees(actorNumbers=[10, 11, 12, 13, 14],
                                                           centerLocation=[0.3, 0.45, 0.80],
                                                           yaw=0,
                                                           xSize=0.17, ySize=0.17, zHeight=0.1,
                                                           wallThickness=0.02,
                                                           floorThickness=0.04,
                                                           wallColor=[0.8, 0.8, 0.8],
                                                           floorColor=[0.5, 0, 0],
                                                           waitForConfirmation=True)

        
        # Create cell rack
        self.cellRack = QLabsBasicShape(self.qlabs)
        self.cellRack.spawn_id(actorNumber=40,
                               location=[0.57, 0.05, 0.85],
                               rotation=[0, 0, 0],
                               scale=[0.1, 0.4, 0.1],
                               configuration=0,
                               waitForConfirmation=True)
        self.cellRack.set_material_properties(color=[0.4, 0.4, 0.4],
                                              roughness=0.1,
                                              metallic=False)
        
        #  ADJUST THIS SECTION TO INCLUDE RANDOM CELL SIZE AND COLOUR
        # Create 4 cell widgets in a row  
    def cell_spawn(self):
        self.cellWidget = QLabsWidget(self.qlabs)
        self.cellWidget.widget_spawn_shadow(enableShadow=True)
        scale = [[0.028, 0.028, 0.06]]
        color = [[0.6, 0, 0]]
        locations = [[0.58, 0.2, 1], [0.58, 0.1, 1], [0.58, 0.0, 1], [0.58, -0.1, 1]]

        for location in locations:
            scale1 = randrange(1)
            color1 = randrange(1)
            self.cellWidget.spawn(location=location,
                             rotation=[0, 0, 0],
                             scale=scale[scale1],
                             configuration= self.cellWidget.CYLINDER,
                             color=color[color1],
                             measuredMass=100,
                             IDTag=0,
                             properties='',
                             waitForConfirmation=True)
# endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# region: Real time model
        
    ##### Start real time model with the arm #####

    def start_real_time_model(self):

        ''' Start the real-time model for QArm. '''

        print("Starting real-time model...")

        qarm_model_path = os.path.join(os.environ['RTMODELS_DIR'], 'QArms/QArm_Spawn0')

        # current_dir = Path(__file__).resolve().parent
        # project_root = current_dir.parent
        # qarm_model_path = project_root / 'libraries' / 'resources' / 'rtmodels' / 'QArms' / 'QArm_Spawn0'

        QLabsRealTime().start_real_time_model(qarm_model_path, actorNumber=3,
                                               additionalArguments='-uri_hil tcpip://localhost:18900 -uri_video tcpip://localhost:18901')

        print("Real-time model started.")

# endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Example usage
# workSpace = QArmWorkspace()
# workSpace.connect_to_qlabs()
# workSpace.initialise_system()
# workSpace.create_workspace()
# workSpace.start_real_time_model()