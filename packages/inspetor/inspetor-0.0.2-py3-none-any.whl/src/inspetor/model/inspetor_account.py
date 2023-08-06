from src.inspetor.model.inspetor_abstract_model import InspetorAbstractModel
from src.inspetor.model.inspetor_address import InspetorAddress
from src.inspetor.exception.model_exception.inspetor_account_exception import InspetorAccountException


class InspetorAccount(InspetorAbstractModel):
    def __init__(self, address = None, timestamp = None):
        self.id = None
        self.name = None
        self.email = None
        self.document = None
        self.phoneNumber = None
        self._address = address
        self._timestamp = timestamp

    def is_valid(self):
        if self.id is None:
            raise InspetorAccountException(
                InspetorAccountException.REQUIRED_ACCOUNT_ID
            )

        if self.email is None:
            raise InspetorAccountException(
                InspetorAccountException.REQUIRED_ACCOUNT_EMAIL
            )

        if self.timestamp is None:
            raise InspetorAccountException(
                InspetorAccountException.REQUIRED_ACCOUNT_TIMESTAMP
            )

    def is_valid_update(self):
        if self.id is None:
            raise InspetorAccountException(
                InspetorAccountException.REQUIRED_ACCOUNT_ID
            )

        if self.timestamp is None:
            raise InspetorAccountException(
                InspetorAccountException.REQUIRED_ACCOUNT_TIMESTAMP
            )

    #To understand this part, please read https://bit.ly/2ywz8PN
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if address is not None:
            address.is_valid()

        self._address = address

    #To understand this part, please read https://bit.ly/2ywz8PN
    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = self.inspetorDateFormatter(timestamp)

    def jsonSerialize(self):
        return {
            "account_id"          : self.encodeData(self.id),
            "account_name"        : self.encodeData(self.name),
            "account_email"       : self.encodeData(self.email),
            "account_document"    : self.encodeData(self.document),
            "account_address"     : self.encodeObject(self.address),
            "account_timestamp"   : self.encodeData(self.timestamp),
            "account_phone_number": self.encodeData(self.phoneNumber)
        }