from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    phone_number: str
    email: str
    first_name: str
    last_name: str
