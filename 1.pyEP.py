import datetime, sys, os
def timeStepHandler(state):
    global get_handle_bool
    if not get_handle_bool:
        get_handle_bool = True
        api_to_csv(state)
    warm_up = ep_api.exchange.warmup_flag(state)

def init():
    sys.path.insert(0, 'C:/EnergyPlusV24-1-0')
    from pyenergyplus.api import EnergyPlusAPI
    global ep_api, get_handle_bool
    get_handle_bool = False
    ep_api = EnergyPlusAPI()
    state = ep_api.state_manager.new_state()
    ep_api.runtime.callback_after_predictor_before_hvac_managers(state, timeStepHandler)
    return state

def api_to_csv(state):
    orig = ep_api.exchange.list_available_api_data_csv(state)
    newFileByteArray = bytearray(orig)
    api_path = os.path.join(os.path.dirname(__file__), 'api_data.csv')
    newFile = open(api_path, "wb")
    newFile.write(newFileByteArray)
    newFile.close()

def main():
    state = init()
    idfFilePath = os.path.join(os.path.dirname(__file__), 'growthChamber_expidf.idf')
    weather_file_path = os.path.join(os.path.dirname(__file__), 'USA_WY_Laramie.Rgnl.AP.725645_TMY3.epw')
    output_path = './ep_trivial'
    sys_args = '-d', output_path, '-w', weather_file_path, idfFilePath
    ep_api.runtime.run_energyplus(state, sys_args)

if __name__ == '__main__':
    main()