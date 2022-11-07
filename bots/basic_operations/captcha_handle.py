from .general_handle import GeneralOperator, Wait, message
from selenium.webdriver.common.by import By
from time import sleep


class WatchForCaptcha(GeneralOperator):
    def __init__(self, driver):
        super().__init__(driver=driver)

    # for captcha that appear on site from time to time
    def on_site(self, captcha_types=None):
        captcha_types = ['rc-anchor-alert', 'hcap-script', 'recaptcha-style'] if captcha_types is not None \
            else captcha_types

        for captcha in captcha_types:
            try:
                self.driver.find_element(By.CLASS_NAME, captcha)
                save_timer = 0
                while save_timer <= Wait.SAFE_EXIT:
                    try:
                        self.driver.find_element(By.CLASS_NAME, captcha)
                        sleep(Wait.MEMORY_SAFE)
                        save_timer += Wait.MEMORY_SAFE
                    except:
                        sleep(Wait.SHORT)
                        break
            except:
                pass

    # for sites that always have captcha after action
    def resolve_confirmation(self, object_to_watch_xpath):
        save_timer = 0
        message('captcha found')
        while save_timer <= Wait.SAFE_EXIT:
            try:
                confirmation_xpath = object_to_watch_xpath
                self.driver.find_element(By.XPATH, confirmation_xpath).click()
                sleep(Wait.SHORT)
                break
            except:
                sleep(Wait.MEMORY_SAFE)
                save_timer += Wait.MEMORY_SAFE

    # for sites that opens another site after resolving captcha
    def site_change(self, site_to_watch):
        save_timer = 0
        message('captcha found')
        while save_timer <= Wait.SAFE_EXIT:
            if site_to_watch not in self.driver.current_url:
                sleep(Wait.SHORT)
                self.close_second_tab()
                break
            else:
                sleep(Wait.MEMORY_SAFE)
                save_timer += Wait.MEMORY_SAFE

if __name__ == '__main__':
    print('Testing space')