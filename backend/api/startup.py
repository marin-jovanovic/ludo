from backend.api.assets.printer import print_logo
from backend.api.comm.scheme_validator import SchemeValidator

class StartupConfig:

    def __init__(self):
        self.scheme_validator = None

    def init_scheme_validator(self, config):
        self.scheme_validator = SchemeValidator(config)

    def get_scheme_validator(self):
        if not self.scheme_validator:
            print("scheme_validator is not initialized")

        return self.scheme_validator

    @staticmethod
    def print_app_logo():
        print_logo()

startup_configuration = StartupConfig()
