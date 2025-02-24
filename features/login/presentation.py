__all__ = ("LoginScreen",)

from features.basescreen import BaseScreen
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class LoginScreen(BaseScreen):
    pass
