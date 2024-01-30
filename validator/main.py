import googlemaps
from typing import Any, Dict
import os

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="is-valid-address", data_type="string")
class IsValidAddress(Validator):
    def __init__(self, **kwargs):
        """Initialise the IsValidAddress validator"""

        super().__init__(kwargs)

        # Get the Google Maps API key from the environment variable
        gmaps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY", None)
        if gmaps_api_key is None:
            raise ValueError(
                "GOOGLE_MAPS_API_KEY environment variable not found. "
                "Please set the environment variable with your Google Maps API key."
            )
        # Initialize the Google Maps client
        self._gmaps_client = googlemaps.Client(key=gmaps_api_key)

    def validate(self, value: str, metadata: Dict) -> ValidationResult:
        """Validate the place using the Google Maps Places API"""

        # Validate an address with address validation
        addressvalidation_result = self._gmaps_client.addressvalidation(
            [value],
            regionCode="US",
            enableUspsCass=True,
        )

        for component in addressvalidation_result["result"]["address"][
            "addressComponents"
        ]:
            if (
                component["componentType"] in ["street_number", "route"]
                and component["confirmationLevel"] != "CONFIRMED"
            ):
                return FailResult(
                    error_message=f"Address {value} is not valid. Please enter a valid address.",
                    fix_value=None,
                )
        return PassResult()
