class By:

    def __init__(self, selector, parent=None):
        if parent is None:
            if isinstance(selector, list):
                self.selectors = selector
            else:
                self.selectors = [selector]
        else:
            if isinstance(selector, list):
                self.selectors = parent + selector
            else:
                self.selectors = parent + [
                    selector
                ]

    def get(self):
        if len(self.selectors) == 1:
            return self.selectors[0]

        return self.selectors

    def find(self, selector: 'By') -> 'By':
        return By(selector, self.get())

    def parents(self, selector: str) -> 'By':
        return By({
            'type': 'jqueryParents',
            'value': selector
        }, self.get())

    def filter(self, selector: str) -> 'By':
        return By({
            'type': 'jqueryFilter',
            'value': selector
        }, self.get())

    @staticmethod
    def css(selector):
        return By._selector('css', selector)

    @staticmethod
    def jquery(selector):
        return By._selector('jquery', selector)

    @staticmethod
    def data_automation_attribute(selector):
        return By._selector('data', selector)

    @staticmethod
    def da_attribute(selector):
        return By._selector('da', selector)

    @staticmethod
    def _selector(selector_type, selector):
        return By(
            {
                'type': selector_type,
                'value': selector
            }
        )
