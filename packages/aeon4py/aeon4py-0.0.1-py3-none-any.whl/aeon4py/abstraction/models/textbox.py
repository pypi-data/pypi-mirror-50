from aeon4py.abstraction.models.web_element import WebElement


class TextBox(WebElement):

    def __init__(self, automation_info, selector):
        super().__init__(automation_info, selector)

    def set(self, text):
        self.automation_info.execute_command('SetCommand', [self.selector.get(), 'TEXT', text])
