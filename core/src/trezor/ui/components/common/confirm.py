from typing import TYPE_CHECKING

import trezorui2

if TYPE_CHECKING:
    from typing import Any, TypeVar

    T = TypeVar("T")

CONFIRMED = trezorui2.CONFIRMED
CANCELLED = trezorui2.CANCELLED
INFO = trezorui2.INFO


def is_confirmed(x: Any) -> bool:
    return x is CONFIRMED
