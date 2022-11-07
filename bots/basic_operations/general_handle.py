import undetected_chromedriver.v2 as uc
import argparse
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def message(msg, team=None):
    date_now = datetime.now().strftime('%H:%M:%S')
    team = team if team is not None else ''
    print('{} --{}--> {}'.format(date_now, team, msg))

def inner_args_control():
    parser = argparse.ArgumentParser()
    parser.add_argument('-browser')
    parser.add_argument('-user_directory')
    parser.add_argument('-profile')
    parser.add_argument('-mode')
    args = parser.parse_args()
    return args


class Wait:
    MEMORY_SAFE = 1
    SHORT = 2
    LONG = 5
    SAFE_EXIT = 1200


class Interface:
    def __init__(self, browser, user_directory, profile):
        self.browser = browser
        self.user_directory = user_directory
        self.profile = profile

    def run_uc(self):
        options = uc.ChromeOptions()
        options.add_argument(f'--profile-directory={self.profile}')
        driver = uc.Chrome(user_data_dir=self.user_directory, options=options)
        return driver

    def run_ff(self):
        options = Options()
        options.add_argument("-profile")
        options.add_argument(f'{self.user_directory}/{self.profile}')
        driver = webdriver.Firefox(options=options)
        return driver

    def init_driver(self):
        return self.run_uc() if self.browser == 'chrome' else self.run_ff()


class GeneralOperator:
    def __init__(self, driver):
        self.driver = driver

    def enter_site(self, login_url, destination_url):
        self.driver.get(login_url)
        save_timer = 0
        while save_timer <= Wait.SAFE_EXIT:
            if destination_url.lower() in self.driver.current_url.lower():
                break
            else:
                sleep(Wait.MEMORY_SAFE)
                save_timer += Wait.MEMORY_SAFE

    def close_second_tab(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            pass

    # shorthand for sites that works with only one run_url
    def prepare_run(self, login_url, destination_url, run_url):
        self.enter_site(login_url, destination_url)
        sleep(Wait.SHORT)

        self.driver.get(run_url)
        sleep(Wait.SHORT)

    def end(self):
        self.driver.quit()

if __name__ == '__main__':
    print('Testing space')