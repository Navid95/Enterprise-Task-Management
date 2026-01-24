from pydantic_core import PydanticCustomError


class DomainValidationError:
    TYPE: str
    MESSAGE_TEMPLATE: str
    RULE: str
    CONTEXT_KEYS: tuple[str, ...]

    @classmethod
    def as_pydantic_error(cls, **context) -> PydanticCustomError:
        missing_ctx_keys = [key for key in cls.CONTEXT_KEYS if key not in context]
        if missing_ctx_keys:
            raise RuntimeError(f"{cls.__name__} Missing Params In Custom Pydantic Exception ({missing_ctx_keys})")
        _context = {
            key: context[key]
            for key in cls.CONTEXT_KEYS
        }
        _context["rule"] = cls.RULE
        return PydanticCustomError(
            cls.TYPE,
            cls.MESSAGE_TEMPLATE,
            _context,
        )


class InvalidStartEndDateRange(DomainValidationError):
    MESSAGE_TEMPLATE = (
        "Start date ({start_date}) must be before the end date ({end_date})"
    )
    TYPE = "invalid_start_end_date_range"
    RULE = "start date time should not be after or equal to end date time"
    CONTEXT_KEYS = ("start_date", "end_date")

