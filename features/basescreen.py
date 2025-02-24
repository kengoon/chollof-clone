from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class BaseScreen(Screen):
    data_source = ObjectProperty(None)
