from guardrails import Guard
from pydantic import BaseModel, Field
from validator import IsValidAddress
import pytest


# Create a pydantic model with a field that uses the custom validator
class ValidatorTestObject(BaseModel):
    address: str = Field(validators=[IsValidAddress(on_fail="exception")])


# Test happy path
@pytest.mark.parametrize(
    "value",
    [
        """
        {
            "address": "1 Hacker Way, Menlo Park, CA"
        }
        """,
        """
        {
            "address": "1600 Amphitheatre Pkwy, Mountain View, CA"
        }
        """,
    ],
)
def test_happy_path(value):
    # Create a guard from the pydantic model
    guard = Guard.from_pydantic(output_class=ValidatorTestObject)
    response = guard.parse(value)
    print("Happy path response", response)
    assert response.validation_passed is True


# Test fail path
@pytest.mark.parametrize(
    "value",
    [
        """
        {
            "address": "300 Hikle Way"
        }
        """,
        """
        {
            "address": "160 Amphetheetre Pkwy"
        }
        """,
        """
        {
            "address": "1800 Owens St"
        }
        """,
    ],
)
def test_fail_path(value):
    # Create a guard from the pydantic model
    guard = Guard.from_pydantic(output_class=ValidatorTestObject)

    with pytest.raises(Exception):
        response = guard.parse(value)
        print("Fail path response", response)
