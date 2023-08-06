from src.inspetor.model.inspetor_abstract_model import InspetorAbstractModel
from src.inspetor.exception.model_exception.inspetor_address_exception import InspetorAddressException

class InspetorAddress(InspetorAbstractModel):
    def __init__(self):
        self.street = None
        self.number = None
        self.zip_code = None
        self.city = None
        self.state = None
        self.country = None
        self.latitude = None
        self.longitude = None

    def is_valid(self):
        if self.street is None:
            raise InspetorAddressException(
                InspetorAddressException.REQUIRED_ADDRESS_STREET
            )

        if self.zip_code is None:
            raise InspetorAddressException(
                InspetorAddressException.REQUIRED_ADDRESS_ZIPCODE
            )

        if self.city is None:
            raise InspetorAddressException(
                InspetorAddressException.REQUIRED_ADDRESS_CITY
            )

        if self.state is None:
            raise InspetorAddressException(
                InspetorAddressException.REQUIRED_ADDRESS_STATE
            )

        if self.country is None:
            raise InspetorAddressException(
                InspetorAddressException.REQUIRED_ADDRESS_COUNTRY
            )

    def jsonSerialize(self):
        return {
            "address_street"   : self.encodeData(self.street),
            "address_number"   : self.encodeData(self.number),
            "address_zip_code" : self.encodeData(self.zip_code),
            "address_city"     : self.encodeData(self.city),
            "address_state"    : self.encodeData(self.state),
            "address_country"  : self.encodeData(self.country),
            "address_latitude" : self.encodeData(self.latitude),
            "address_longitude": self.encodeData(self.longitude)
        }
