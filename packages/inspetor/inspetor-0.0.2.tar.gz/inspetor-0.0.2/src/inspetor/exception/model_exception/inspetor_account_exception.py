from src.inspetor.exception.exception_abstract import ExceptionAbstract

import logging


class InspetorAccountException(ExceptionAbstract):
    status_code = 700
    severity    = logging.CRITICAL

    REQUIRED_ACCOUNT_ID = {
        'message': 'id is a required property. It can\'t be null.',
        'code'   : 7001,
    }

    REQUIRED_ACCOUNT_EMAIL = {
        'message': 'email is a required property. It can\'t be null on creation.',
        'code'   : 7002,
    }

    REQUIRED_ACCOUNT_TIMESTAMP = {
        'message': 'timestamp is a required property. It can\'t be null.',
        'code'   : 7003,
    }