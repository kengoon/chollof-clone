from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ColorProperty, OptionProperty


class Theme:
    bg_color = ColorProperty()
    bg_color_light = ColorProperty("#FFFFFF")
    bg_color_dark = ColorProperty("#000000")
    primary_color = ColorProperty()
    primary_color_light = ColorProperty("#8AC3D4")
    primary_color_dark = ColorProperty("#8AC3D4")
    secondary_color = ColorProperty()
    secondary_color_light = ColorProperty()
    secondary_color_dark = ColorProperty()
    accent_color = ColorProperty()
    accent_color_light = ColorProperty()
    accent_color_dark = ColorProperty()
    text_color = ColorProperty()
    text_color_light = ColorProperty("#3F3F41")
    text_color_dark = ColorProperty("#FFFFFF")
    theme_style = OptionProperty(None, options=["Light", "Dark"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_style = App.get_running_app().theme_style
        App.get_running_app().bind(theme_style=self.setter("theme_style"))

    def on_theme_style(self, *args):
        self.set_theme()

    def set_theme(self, *args):
        if self.theme_style == "Light":
            self.bg_color = self.bg_color_light
            self.primary_color = self.primary_color_light
            self.secondary_color = self.secondary_color_light
            self.accent_color = self.accent_color_light
            self.text_color = self.text_color_light
        else:
            self.bg_color = self.bg_color_dark
            self.primary_color = self.primary_color_dark
            self.secondary_color = self.secondary_color_dark
            self.accent_color = self.accent_color_dark
            self.text_color = self.text_color_dark

        Window.clearcolor = self.bg_color
