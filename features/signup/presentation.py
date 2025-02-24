__all__ = ("SignupScreen",)

from features.basescreen import BaseScreen
from kivy.lang import Builder
from os.path import join, dirname, basename
# from sjfirebase.tools.mixin import PhoneMixin, FirestoreMixin
from components.otp import OtpSheet

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class SignupScreen(BaseScreen):
    def create_account(self):
        country_code = self.ids.country_code.text
        phone_number = self.ids.phone_number.text
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        email = self.ids.email.text

        OtpSheet().open()





