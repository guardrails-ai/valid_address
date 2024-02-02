from guardrails import Guard
from pydantic import BaseModel, Field
from validator import IsValidAddress


class ValidatorTestObject(BaseModel):
    address: str = Field(validators=[IsValidAddress(on_fail="exception")])


# Create a guard from the pydantic model
guard = Guard.from_pydantic(output_class=ValidatorTestObject)

print("Testing validator happy path...")
TEST_PASS_OUTPUT = """
{
  "address": "1 Hacker Way, Menlo Park, CA"
}
"""
raw_output, guarded_output, *rest = guard.parse(TEST_PASS_OUTPUT)
print("Validated output: ", guarded_output)
print("#" * 50)

print("Testing validator fail path 1...")
TEST_FAIL_OUTPUT = """
{
    "address": "300 John Hikle Ave"
}
"""

try:
    guard.parse(TEST_FAIL_OUTPUT)
    print("Failed to fail validation when it was supposed to")
except Exception as e:
    print("Successfully failed validation when it was supposed to")
print("#" * 50)

print("Testing validator fail path 2...")
TEST_FAIL_OUTPUT = """
{
    "address": "1800 Owens St"
}
"""

try:
    guard.parse(TEST_FAIL_OUTPUT)
    print("Failed to fail validation when it was supposed to")
except Exception as e:
    print("Successfully failed validation when it was supposed to")
print("#" * 50)

print("Testing validator fail path 3...")
TEST_FAIL_OUTPUT = """
{
    "address": "1600 Ampetheakre Pkwy"
}
"""

try:
    guard.parse(TEST_FAIL_OUTPUT)
    print("Failed to fail validation when it was supposed to")
except Exception as e:
    print("Successfully failed validation when it was supposed to")
