class WebElement:

    def __init__(self, automation_info, selector):
        self.automation_info = automation_info
        self.selector = selector

    def click(self):
        self.automation_info.execute_command('ClickCommand', [self.selector.get()])
