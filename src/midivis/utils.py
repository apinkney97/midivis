from typing import Any

from rich.console import Console

_VERBOSITY = 0
_CONSOLE = Console()


def get_console() -> Console:
    return _CONSOLE


def set_verbosity(verbosity: int) -> None:
    global _VERBOSITY
    _VERBOSITY = verbosity


def get_verbosity() -> int:
    return _VERBOSITY


def log(verbosity: int, *args: Any, **kwargs: Any) -> None:
    if verbosity <= get_verbosity():
        _CONSOLE.log(*args, **kwargs)


class VolumeController:
    """
    TODO: I2C integration with amplifier on Raspberry Pi

    >>> import smbus
    >>> DEVICE_BUS = 1
    >>> DEVICE_ADDR = 0x4b
    >>> bus = smbus.SMBus(DEVICE_BUS)
    >>> bus.write_byte_data(DEVICE_ADDR, 0x00, 0x3F)
    """

    def __init__(self, initial_volume: int = 32):
        self._volume = 0

        self.volume = initial_volume

    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, volume: int) -> None:
        self._volume = max(0, min(63, volume))

    def inc(self, increment: int = 1) -> bool:
        # Returns True if the volume changed, or false if it capped out (at either end)
        before = self.volume
        self.volume = before + increment
        return before != self.volume

    def dec(self, decrement: int = 1) -> bool:
        return self.inc(-decrement)
