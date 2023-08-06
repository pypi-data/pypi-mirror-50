import sys
import allure
from allure_commons.types import AttachmentType


class Screenshot:
    def __init__(self, driver):
        self.driver = driver

    def screen(self):
        if sys.exc_info():
            allure.attach(self.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        pass
