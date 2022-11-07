import os
import argparse
import pandas as pd
from bots import *
import importlib
from bots.basic_operations.general_handle import Interface
from data.market_info import GetMarketInfo, DataManager


class Profiles:
    DB_NAME = 'wallet.db'
    UC_USER_DATA_DIR = '/home/user_dir/.config/google-chrome'
    FF_USER_DATA_DIR = '/home/user_dir/.mozilla/firefox'
    UC_PROFILES_NAME = [('Default', 'yellow')]
    FF_PROFILES_NAME = [('ff_code.user_typed_name', 'red'),
                        ('ff_code.user_typed_name', 'purple'),
                        ('ff_code.user_typed_name', 'green')]


class BotsMenu(Profiles):
    def __init__(self):
        self.ff_profiles = [p[1] for p in self.FF_PROFILES_NAME]
        self.uc_profiles = [p[1] for p in self.UC_PROFILES_NAME]
        self.teams = self.ff_profiles + self.uc_profiles
        self.actions = [a.replace('.py', '') for a in os.listdir('bots') if a.endswith('py') and not a.startswith('_')]
        self.MISSION_SCHEMA = dict.fromkeys(self.teams, [])

    def print_menu(self):
        print('MOTHERLODE 4K')
        print('Command schema: r13 y26 (red team, bot 1 nad 3)')
        for team in self.teams:
            browser = 'UC' if team == 'yellow' else 'FF'
            print(f' {team[0]}. {team} ({browser})')
        print('Sites:')
        [print(' {}. {}'.format(self.actions.index(a) + 1, a)) for a in self.actions]

    def read_command(self, external_command):
        read = input('Command: ') if external_command is None else external_command
        tasks = read.split(' ')
        if read == 'clear':
            os.system('clear')
            quit()

        for t in tasks:
            team = t[0]
            for m in self.MISSION_SCHEMA:
                if m.startswith(team):
                    for i in range(1, len(t)):
                        self.MISSION_SCHEMA[m].append(self.actions[int(t[i]) - 1])

        return self.MISSION_SCHEMA

    def repair_chrome(self):
        print('This will irreversibly erase all profiles in Google Chrome')
        decision = input('Continue? [y/n]: ')
        if decision == 'y':
            os.system(f'rm -rf {self.UC_USER_DATA_DIR}')
            print('Google Chrome data erased')
        else:
            print('Google Chrome data preserved')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', action='store_true', help='print action menu')
    parser.add_argument('-c', help='commands in format: r13 y26 (red team, bot 1 nad 3) as string')
    parser.add_argument('-r', action='store_true', help='clear Google Chrome congif directory')
    parser.add_argument('-w', action='store_true', help='check wallets on sites')
    parser.add_argument('-market', help='fetch market data, format: history/now/both coin1 coin2 as string')

    args = parser.parse_args()

    os.system('export PATH=$PATH:/home/user_dir/Downloads')

    menu = BotsMenu()

    if args.r:
        menu.repair_chrome()
        quit()

    if args.w:
        interface = Interface('chrome', Profiles.UC_USER_DATA_DIR, Profiles.UC_PROFILES_NAME[0][0])
        driver = interface.init_driver()
        db = DataManager(Profiles.DB_NAME)
        for action in menu.actions:
            try:
                task_module = importlib.import_module(f'bots.{action}')
                balance = task_module.check_wallet(driver)
                destination_table = 'balance_faucetpay' if action == 'faucetpay' else 'balance_sites'
                db.save_table(pd.DataFrame([balance]), destination_table)
            except:
                pass

        driver.close()
        quit()

    if args.m:
        menu.print_menu()
        quit()

    if args.market is not None:
        command = args.market.split(' ')
        mode = command[0]
        for coin in range(1, len(command)):
            market = GetMarketInfo(command[coin], Profiles.DB_NAME)
            if mode in ['history', 'both']:
                market.historical()

            if mode in ['now', 'both']:
                market.last_week()



    # r4 p6 g51 y36
    if args.c is not None:
        mission_schema = menu.read_command(args.c)
        for team in mission_schema:
            if len(mission_schema[team]) > 0:
                flow = team
                for action in mission_schema[team]:
                    flow += f' {action}'
                os.system(f'xterm -bg {team} -e python3 deploy.py -flow "{flow}" &')





