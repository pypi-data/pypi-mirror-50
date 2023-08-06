class Browser:

    def __init__(self, automation_info):
        self.automation_info = automation_info

    def go_to(self, url):
        self.automation_info.execute_command('GoToUrlCommand', [url])

    def quit(self):
        self.automation_info.quit_session()
