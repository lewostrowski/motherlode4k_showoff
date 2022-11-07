from .general_handle import GeneralOperator, Wait, message
from selenium.webdriver.common.by import By
from time import sleep


class WatchAds(GeneralOperator):
    def __init__(self, driver):
        super().__init__(driver=driver)

    # watch button does not change xpath
    def run_static_xpath(self, ad_xpath, id_instead=None):
        if type(ad_xpath) == list and id_instead is None:
            for xpath in ad_xpath:
                try:
                    self.driver.find_element(By.XPATH, xpath).click()
                    break
                except:
                    pass
        elif type(id_instead) == str:
            self.driver.find_element(By.XPATH, id_instead).click()
        else:
            self.driver.find_element(By.XPATH, ad_xpath).click()

        message('opening ad')
        sleep(Wait.SHORT)

    # check timer on site
    def check_timer(self, value_to_watch, timer_xpath=None, timer_id=None):
        save_timer = 0
        message('checking timer')
        while save_timer <= Wait.SAFE_EXIT:
            if timer_id is not None:
                t = self.driver.find_element(By.ID, timer_id).text
            else:
                t = self.driver.find_element(By.XPATH, timer_xpath).text

            if str(t).lower() == str(value_to_watch).lower():
                sleep(Wait.SHORT)
                break
            else:
                sleep(Wait.MEMORY_SAFE)
                save_timer += Wait.MEMORY_SAFE

    # check changing style on site
    def check_style(self, value_to_watch, element_xpath=None, element_id=None, element_class=None):
        save_timer = 0
        message('checking timer')
        while save_timer <= Wait.SAFE_EXIT:
            if element_id is not None:
                t = self.driver.find_element(By.ID, element_id).text
            if element_class is not None:
                t = self.driver.find_element(By.CLASS_NAME, element_class).text
            else:
                t = self.driver.find_element(By.XPATH, element_xpath).text

            if str(t).lower() == str(value_to_watch).lower():
                sleep(Wait.SHORT)
                break
            else:
                sleep(Wait.MEMORY_SAFE)
                save_timer += Wait.MEMORY_SAFE

    # check title tag in page's head
    def check_title(self, value_to_watch, error_values, second_tab=False, improve_accuracy=False):
        save_timer = 0
        error_watch = 0
        message('checking timer')
        while save_timer <= Wait.SAFE_EXIT:
            if value_to_watch.lower().strip() == self.driver.title.lower().strip() and improve_accuracy:
                sleep(Wait.SHORT)
                if second_tab:
                    self.close_second_tab()
                break
            elif value_to_watch.lower().strip() in self.driver.title.lower().strip() and not improve_accuracy:
                sleep(Wait.SHORT)
                if second_tab:
                    self.close_second_tab()
                break
            else:
                sleep(Wait.MEMORY_SAFE)
                save_timer += Wait.MEMORY_SAFE

            for e in error_values:
                if e.lower() == self.driver.title.lower():
                    error_watch += 2
                    sleep(Wait.MEMORY_SAFE)

            if error_watch > 10:
                if second_tab:
                    self.close_second_tab()
                break

if __name__ == '__main__':
    print('Testing space')