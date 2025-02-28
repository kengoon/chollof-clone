__all__ = ("SignupScreen",)

from kivy.properties import NumericProperty
from features.basescreen import BaseScreen
from kivy.lang import Builder
from os.path import join, dirname, basename

from sjfirebase.jclass.filter import Filter
from sjfirebase.tools.mixin import PhoneMixin, FirestoreMixin, AuthMixin, UserMixin
from components.otp import OtpSheet
from kivy.clock import mainthread, Clock, ClockEvent

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))
clock: ClockEvent = None


class SignupScreen(BaseScreen, AuthMixin, PhoneMixin, FirestoreMixin, UserMixin):
    _timeout = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global clock
        self.verification_id = None
        self.token = None
        self._countdown_callback = lambda _: setattr(self, "_timeout", self._timeout - 1)
        clock = Clock.create_trigger(self._countdown_callback, 1, True)
        self.bind(_timeout=lambda _, tmo: clock.cancel() if tmo == 0 else None)

    def prepare_account_creation(self):
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
                self.toast("Account already exist, please login")
                self.manager.current = "login screen"
            else:
                self.create_account()
        else:
            self.toast(data)

    @mainthread
    def create_account(self):
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        email = self.ids.email.text
        phone_number = self.ids.country_code.text + self.ids.phone_number.text

        data = dict(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
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
                        self.set_document(f"users/{self.get_uid()}", data, lambda *_: None),
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
