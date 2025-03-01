from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.properties import ObjectProperty

from components.bar import win_md_bnb
from components.transition import SharedAxisTransition
from ui.theme import ThemeManager
from components.factory_register import register_factory
from features.screenmanager import AppScreenManager
from kivy.lang import Builder

Loader.error_image = "assets/images/transparent.png"
Loader.loading_image = "assets/images/transparent.png"
Window.softinput_mode = "below_target"
Builder.load_file("imports.kv")
register_factory()


class ChollofApp(App):
    theme_cls = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        # self.theme_cls.theme_style = "Dark"

    def build(self):
        sm = AppScreenManager(transition=SharedAxisTransition())
        if platform == "android":
            from sjfirebase.tools.mixin import UserMixin
            if user := UserMixin().get_current_user():
                user.reload()
                sm.current = "restaurant screen"
                return sm
        sm.current = "login screen"
        return sm

    def on_start(self):
        win_md_bnb.create_bnb(
            tabs=[
                {
                    "icon": "storefront",
                    "icon_variant": "storefront-outline",
                    "text": "Restaurants",
                    "active": True,
                },
                # {
                #     "icon": "bike-fast",
                #     "icon_variant": "bike-fast",
                #     "text": "Order",
                #     "active": False,
                #     "on_release": lambda _: self.add_screen("order screen")
                # },
                {
                    "icon": "cog",
                    "icon_variant": "cog-outline",
                    "text": "Settings",
                }
            ],
        )


if __name__ == '__main__':
    ChollofApp().run()

