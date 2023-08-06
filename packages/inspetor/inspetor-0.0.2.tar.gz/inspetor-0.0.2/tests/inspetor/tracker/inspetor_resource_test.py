from datetime import datetime
import pytest

from src.inspetor_resource import InspetorResource
from tests.inspetor.tracker.default_models import DefaultModels


class TestInspetorResource:
    def get_default_inspetor_resource(self):
        inspetor = InspetorResource(
            {
                "APP_ID":"123",
                "TRACKER_NAME":"123",
                "DEV_ENV":True,
                "INSPETOR_ENV":True
            }
        )
        return inspetor

    def test_account(self):
        default_models = DefaultModels()
        inspetor = self.get_default_inspetor_resource()
        account = default_models.get_default_account()

        inspetor.track_account_action(account, "account_create")

    def test_event(self):
        default_models = DefaultModels()
        inspetor = self.get_default_inspetor_resource()
        event = default_models.get_default_event()

        inspetor.track_event_action(event, "event_create")

    def test_auth(self):
        default_models = DefaultModels()
        inspetor = self.get_default_inspetor_resource()
        auth = default_models.get_default_auth()

        inspetor.track_account_auth_action(auth, "account_login")

    def test_sale(self):
        default_models = DefaultModels()
        inspetor = self.get_default_inspetor_resource()
        sale = default_models.get_default_sale()

        inspetor.track_sale_action(sale, "sale_create")

    def test_pass(self):
        default_models = DefaultModels()
        inspetor = self.get_default_inspetor_resource()
        passw = default_models.get_default_pass_recovery()

        inspetor.track_password_recovery_action(passw, "password_reset")





