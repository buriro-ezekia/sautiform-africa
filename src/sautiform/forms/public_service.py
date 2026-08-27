"""Public-service form schema and validation rules."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class PublicServiceForm:
    district: str | None = None
    occupation: str | None = None
    household_size: int | None = None
    service_request: str | None = None

    REQUIRED_FIELDS = ("district", "occupation", "household_size", "service_request")

    def missing_fields(self) -> list[str]:
        return [name for name in self.REQUIRED_FIELDS if getattr(self, name) in (None, "")]

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.household_size is not None and not 1 <= self.household_size <= 50:
            errors.append("household_size must be between 1 and 50")
        return errors

    def to_dict(self) -> dict[str, str | int | None]:
        return asdict(self)
