import os, sys
sys.path.insert(0, 'C:/EnergyPlusV24-1-0')
from pyenergyplus.api import EnergyPlusAPI

ep_api = EnergyPlusAPI()
state = ep_api.state_manager.new_state()
psychrometricFunc = ep_api.functional.psychrometrics(state)

epw_Template_file_path = 'USA_WY_Laramie.Rgnl.AP.725645_TMY3.epw'

with open(epw_Template_file_path, 'r') as f:
    lines = f.readlines()
    dryBulbC = 23
    RHPercentage = 10
    pressPa = 100700
    humidityRatio = psychrometricFunc.humidity_ratio_c(state, dryBulbC, RHPercentage/100, pressPa)
    dewPoint = psychrometricFunc.dew_point(state, humidityRatio, pressPa)
    for rowIdx in range(8, len(lines)):
        lines[rowIdx] = lines[rowIdx].split(',')
        lines[rowIdx][6] = str(dryBulbC)
        lines[rowIdx][7] = str(dewPoint)
        lines[rowIdx][8] = str(RHPercentage)
        lines[rowIdx] = ','.join(lines[rowIdx])

with open('UWYO.SI.Building.Indoor.epw', 'w') as f:
    f.writelines(lines)


