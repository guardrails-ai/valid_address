from guardrails import Guard
from pydantic import BaseModel, Field
from validator import IsValidAddress


class ValidatorTestObject(BaseModel):
    test_val: str = Field(validators=[IsValidAddress(on_fail="exception")])


TEST_PASS_OUTPUT = """
{
  "test_val": "1 Hacker Way, Menlo Park, CA"
}
"""


guard = Guard.from_pydantic(output_class=ValidatorTestObject)
raw_output, guarded_output, *rest = guard.parse(TEST_PASS_OUTPUT)
print("Validated output: ", guarded_output)


TEST_FAIL_OUTPUT = """
{
"test_val": "300 John Hikle Ave"
}
"""

try:
    guard.parse(TEST_FAIL_OUTPUT)
    print("Failed to fail validation when it was supposed to")
except Exception as e:
    print("Successfully failed validation when it was supposed to")
