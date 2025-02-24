__all__ = ("OtpScreen",)

from kivy.clock import Clock
from features.basescreen import BaseScreen
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class OtpScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cbtn = self.ids.cbtn
        self.clock = Clock.create_trigger(
            lambda _: setattr(cbtn, "countdown", cbtn.countdown - 1),
            timeout=1,
            interval=True
        )
        self.clock()
        cbtn.bind(countdown=lambda _, ctd: self.clock.cancel() if ctd == 0 else None)
