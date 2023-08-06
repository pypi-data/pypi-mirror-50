from aeon4py.abstraction.models.web_element import WebElement


class Button(WebElement):

    def __init__(self, automation_info, selector):
        super().__init__(automation_info, selector)
