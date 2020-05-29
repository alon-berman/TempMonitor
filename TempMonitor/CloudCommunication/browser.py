from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

_CHROME_OPTIONS = \
    ['start-maximized', 'enable-automation', '--headless', '--no-sandbox', '--disable-infobars',
     '--disable-dev-shm-usage', '--disable-browser-side-navigation', '--disable-gpu']


class Browser:
    """
    A Singleton function representing a Chrome browser object.
    """

    class __Browser:
        def __init__(self, *args):
            self.options = Options()
            self.prepare_options()
            self.obj = Chrome(options=self.options)

        def prepare_options(self):
            for option in _CHROME_OPTIONS:
                self.options.add_argument(option)

    instance = None

    def __init__(self, *args):
        if not Browser.instance:
            Browser.instance = Browser.__Browser(args)
        else:
            Browser.instance.val = args

    def __getattr__(self, name):
        return getattr(self.instance.obj, name)

    def __enter__(self):
        return self.obj

    def __exit__(self, exc_type, xc_val, exc_tb):
        self.obj.close()