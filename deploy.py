import argparse
import importlib
import os
from bots import *
from bots_commander import BotsMenu
from bots.basic_operations.general_handle import Interface

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-flow', help='multi-driver control command, for internal and testing purpose')
    args = parser.parse_args()
    os.system('export PATH=$PATH:/home/capitalturtle/Downloads') # os nie zadzialal

    # team app1 app2
    menu = BotsMenu()
    flow = args.flow.split(' ')
    browser = 'chrome' if flow[0] == 'yellow' else 'firefox'
    user_data_dir = menu.UC_USER_DATA_DIR if browser == 'chrome' else menu.FF_USER_DATA_DIR

    teams = menu.FF_PROFILES_NAME + menu.UC_PROFILES_NAME
    for team in teams:
        if team[1] == flow[0]:
            interface = Interface(browser, user_data_dir, team[0])
            print(interface.user_directory, interface.profile)
            driver = interface.init_driver()
            for i in range(1, len(flow)):
                task_module = importlib.import_module(f'bots.{flow[i]}')
                try:
                    task_module.watch_ptc(driver)
                except:
                    pass


    confirm = input('Press any key to exit')
    if len(confirm) > 0:
        driver.close()
        quit()