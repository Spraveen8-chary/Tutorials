from pydantic import BaseModel, EmailStr, HttpUrl, IPvAnyAddress, SecretStr, PositiveInt
from typing import List

# Note: Using EmailStr requires the 'email-validator' package.
# We included pydantic[email] in requirements.txt to handle this.

class Company(BaseModel):
    name: str
    website: HttpUrl
    support_email: EmailStr
    office_ip: IPvAnyAddress
    # SecretStr hides the value when printing or exporting to JSON
    api_key: SecretStr
    # PositiveInt ensures the value is > 0
    employee_count: PositiveInt

# Example data
data = {
    "name": "Tech Corp",
    "website": "https://techcorp.com",
    "support_email": "help@techcorp.com",
    "office_ip": "192.168.1.1",
    "api_key": "sk_test_12345",
    "employee_count": 150
}

company = Company(**data)

print(f"Company: {company.name}")
print(f"Website: {company.website}")
print(f"Support Email: {company.support_email}")
print(f"IP: {company.office_ip}")

# Notice how api_key is masked
print(f"API Key (masked): {company.api_key}")
# To get the actual value, use get_secret_value()
print(f"API Key (actual): {company.api_key.get_secret_value()}")

# Invalid data example
try:
    data = {
        "name": "Tech Corp",
        "website": "https://techcorp.com",
        "support_email": "not-an-email",
        "office_ip": "192.168.1.1",
        "api_key": "sk_test_12345",
        "employee_count": -5
    }
    Company(**data)
except Exception as e:
    print(f"\nCaught Expected Advanced Type Errors:\n{e}")
