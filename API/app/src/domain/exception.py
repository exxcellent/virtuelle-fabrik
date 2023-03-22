
from attr import define


@define
class DomainException(Exception):
    message: str
