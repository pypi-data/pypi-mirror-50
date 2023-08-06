import array as arr
import json
import os
import time
import unicodedata
from configparser import ConfigParser

from src.inspetor.model.inspetor_abstract_model import InspetorAbstractModel
from src.inspetor.inspetor_json_encoder import AbstractModelEncoder

from snowplow_tracker import logger
from snowplow_tracker import SelfDescribingJson
from snowplow_tracker import Subject, Tracker, Emitter


class InspetorResource:
    def __init__(self, configDict):
        """
        Initialize service
        """
        with open('src/config.json') as config_file:
            self.defaultConfig = json.load(config_file)
        self.companyConfig = configDict
        self.tracker = None
        self.emitter = None
        self.subject = None

        self.verify_tracker()

    def verify_tracker(self):
        """Verify if tracker already exists"""
        if self.tracker is None:
            self.setup_tracker()

        return True

    def setup_tracker(self):
        """Setup an instance of a tracker"""
        self.companyConfig = self.setup_config(self.companyConfig)
        self.emitter = Emitter(
            self.companyConfig["COLLECTOR_HOST"],
            protocol = self.companyConfig["PROTOCOL"],
            port = self.companyConfig["PORT"],
            method = self.companyConfig["EMIT_METHOD"],
            buffer_size = self.companyConfig["BUFFER_SIZE"]
        )
        self.subject = Subject()
        self.tracker = Tracker(
            emitters = self.emitter,
            subject = self.subject,
            namespace = self.companyConfig["TRACKER_NAME"],
            app_id = self.companyConfig["APP_ID"],
            encode_base64 = self.companyConfig["ENCODE64"]
        )

    def setup_config(self, config):
        """Setup config with company and default config"""
        if config['TRACKER_NAME'] is None or \
            config['APP_ID'] is None:
            return

        keys = [
            'COLLECTOR_HOST',
            'PROTOCOL',
            'EMIT_METHOD',
            'BUFFER_SIZE',
            'DEBUG_MODE',
            'ENCODE64',
            'PORT'
        ]

        for key in keys:
            config[key] = self.defaultConfig[key]

        if "DEV_ENV" in config:
            if config["DEV_ENV"] == True:
                config["COLLECTOR_HOST"] = self.defaultConfig["COLLECTOR_HOST_DEV"]

        if "INSPETOR_ENV" in config:
            if config["INSPETOR_ENV"] == True:
                config["COLLECTOR_HOST"] = 'test'

        return config

    def track_described_event(
        self,
        schema,
        data,
        context = None,
        action = None
    ):
        """
        Track a described event

        Keyword Arguments:
        schema     -- string
        data       -- array
        context    -- string
        action     -- string
        """
        self.verify_tracker()
        try:
            data = data.jsonSerialize()
        except Exception as encoder_fail:
            self.report_non_descriptible_call(schema)
            return False

        self.tracker.track_self_describing_event(
            SelfDescribingJson(
                schema,
                data
            ),
            [
                SelfDescribingJson(
                    context,
                    {
                        'action': action
                    }
                ),
            ],
            self.get_normalized_timestamp()
        )

    def report_non_descriptible_call(self, schema):
        """
        Track a non described event

        Keyword Arguments:
        schema     -- string
        """
        self.verify_tracker()

        self.tracker.track_self_describing_event(
            SelfDescribingJson(
                self.defaultConfig["INGRESSE_SERIALIZATION_ERROR"],
                {
                    'intendedSchemaId': schema
                }
            ),
            [],
            self.get_normalized_timestamp()
        )


    def track_account_action(self, data, action):
        """
        Track an Account action

        Keyword Arguments:
        data       -- InspetorAccount
        action     -- string
        """
        if action == "account_create":
            data.is_valid()

        data.is_valid_update()

        self.track_described_event(
            self.defaultConfig["INSPETOR_ACCOUNT_SCHEMA"],
            data,
            self.defaultConfig["INSPETOR_CONTEXT_SCHEMA"],
            action
        )

    def track_sale_action(self, data, action):
        """
        Track a Sale action

        Keyword Arguments:
        data       -- InspetorSale
        action     -- string
        """
        self.track_described_event(
            self.defaultConfig["INSPETOR_SALE_SCHEMA"],
            data,
            self.defaultConfig["INSPETOR_CONTEXT_SCHEMA"],
            action
        )

    def track_event_action(self, data, action):
        """
        Track an Event action

        Keyword Arguments:
        data       -- InspetorEvent
        action     -- string
        """
        self.track_described_event(
            self.defaultConfig["INSPETOR_EVENT_SCHEMA"],
            data,
            self.defaultConfig["INSPETOR_CONTEXT_SCHEMA"],
            action
        )

    def track_item_transfer_action(self, data, action):
        """
        Track an ItemTransfer action

        Keyword Arguments:
        data       -- ItemTransfer
        action     -- string
        """
        self.track_described_event(
            self.defaultConfig["INSPETOR_TRANSFER_SCHEMA"],
            data,
            self.defaultConfig["INSPETOR_CONTEXT_SCHEMA"],
            action
        )

    def track_account_auth_action(self, data, action):
        """
        Track an AccountAuth action

        Keyword Arguments:
        data       -- AccountAuth
        action     -- string
        """
        self.track_described_event(
            self.defaultConfig["INSPETOR_AUTH_SCHEMA"],
            data,
            self.defaultConfig["INSPETOR_CONTEXT_SCHEMA"],
            action
        )

    def track_password_recovery_action(self, data, action):
        """
        Track an PasswordRecovery action

        Keyword Arguments:
        data       -- PasswordRecovery
        action     -- string
        """
        self.track_described_event(
            self.defaultConfig["INSPETOR_PASS_RECOVERY_SCHEMA"],
            data,
            self.defaultConfig["INSPETOR_CONTEXT_SCHEMA"],
            action
        )

    def flush(self):
        """
        Flush trackers
        """
        self.t.flush(False)

    def get_normalized_timestamp(self):
        """
        Get correct timestamp
        """
        return int(time.time())*1000

    def get_normalized_data(self, data):
        """
        Format string to replace non-ascii characters
        """
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8')
