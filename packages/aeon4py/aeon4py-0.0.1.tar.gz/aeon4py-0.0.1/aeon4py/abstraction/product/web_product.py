from aeon4py.abstraction.product.browser import Browser


class WebProduct:

    def __init__(self, adapter, settings=None):
        self.automation_info = adapter.get_session(settings)
        self.browser = Browser(self.automation_info)

        if settings is not None and 'aeon.environment' in settings:
            self.browser.go_to(settings['aeon.environment'])
