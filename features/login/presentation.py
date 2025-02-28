__all__ = ("LoginScreen",)

from kivy.properties import NumericProperty

from components.otp import OtpSheet
from features.basescreen import BaseScreen
from kivy.lang import Builder
from os.path import join, dirname, basename
from sjfirebase.tools.mixin import PhoneMixin, FirestoreMixin, AuthMixin, UserMixin
from kivy.clock import Clock, ClockEvent, mainthread

from sjfirebase.jclass.filter import Filter

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))
clock: ClockEvent = None


class LoginScreen(BaseScreen, AuthMixin, PhoneMixin, FirestoreMixin, UserMixin):
    _timeout = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global clock
        self.verification_id = None
        self.token = None
        self._countdown_callback = lambda _: setattr(self, "_timeout", self._timeout - 1)
        clock = Clock.create_trigger(self._countdown_callback, 1, True)
        self.bind(_timeout=lambda _, tmo: clock.cancel() if tmo == 0 else None)

    def prepare_login(self):
        if self.ids.spinner.active:
            return
        if self._timeout:
            return
        self.ids.spinner.active = True

        phone_number = self.ids.country_code.text + self.ids.phone_number.text
        filter_ = Filter.equalTo("phone_number", phone_number)
        self.where("users", filter_, self.check_account_exist)

    @mainthread
    def check_account_exist(self, success, data):
        if success:
            if data:
                self.login()
            else:
                self.toast("This user doesn't have any account, please sign up.")
                self.manager.current = "signup screen"
        else:
            self.toast(data)

    @mainthread
    def login(self):
        phone_number = self.ids.country_code.text + self.ids.phone_number.text
        timeout = 60
        listener = self.set_phone_state_callbacks(
            on_code_sent=lambda verification_id, token: (
                setattr(self, "verification_id", verification_id),
                setattr(self, "token", token),
                mainthread(lambda: setattr(self.ids.spinner, "active", False))(),
                sheet.open(),
                mainthread(lambda: setattr(self, "_timeout", timeout))(),
                clock()
            ),
            on_verification_completed=lambda credential:
            self.sign_in_with_credential(
                credential,
                lambda suc, err: (
                    (
                        sheet.stop_spinner(),
                        sheet.dismiss(),
                    ) if suc
                    else (
                        sheet.stop_spinner(),
                        self.toast(err)
                    )
                )
            ),
            on_verification_failed=lambda error: (
                self.toast(error),
                mainthread(lambda: setattr(self.ids.spinner, "active", False))()
            )
        )

        sheet = OtpSheet(
            timeout=timeout,
            on_submit_otp=lambda _, otp: self.sign_in_with_credential(
                self.verify_number_with_code(self.verification_id, otp),
                lambda suc, err: (
                    (
                        sheet.stop_spinner(),
                        sheet.dismiss(),
                        mainthread(lambda: setattr(self.manager, "current", "restaurant screen"))()
                    ) if suc
                    else (
                        sheet.stop_spinner(),
                        self.toast(err)
                    )
                )
            ),
            on_resend_otp=lambda _: self.resend_verification_code(
                phone_number,
                timeout,
                self.token,
                listener,
            )
        )

        self.start_phone_number_verification(
            phone_number,
            timeout,
            listener,
        )
