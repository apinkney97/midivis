"""
Helpers to call the WLED API
"""

import colorsys
import functools
import itertools
import time
from typing import Any, Iterable, NamedTuple

import requests
from more_itertools import run_length

HOST = "192.168.1.152"
LEDS_WIDTH = 100
LEDS_HEIGHT = 16
NUM_LEDS = LEDS_WIDTH * LEDS_HEIGHT


class RGBColor(NamedTuple):
    # Values must be 0-255
    r: int
    g: int
    b: int

    @functools.cache
    def __str__(self) -> str:
        return f"{self.r:02X}{self.g:02X}{self.b:02X}"

    @classmethod
    @functools.cache
    def from_hsv(cls, hue: float, sat: float, val: float) -> "RGBColor":
        # h/s/v in range 0-1
        r, g, b = (int(x * 255) for x in colorsys.hsv_to_rgb(hue, sat, val))
        return cls(r, g, b)


OFF = RGBColor.from_hsv(0, 0, 0)


def _set_state(data: dict[str, Any]) -> None:
    """Raw call to /json/state on the WLED API."""
    # import json; print(json.dumps(data)); return
    resp = requests.post(f"http://{HOST}/json/state", json=data)
    resp.raise_for_status()


def set_leds_all(colors: Iterable[RGBColor]) -> None:
    """Sets the LEDs to the specified colors."""
    # See https://kno.wled.ge/interfaces/json-api/#per-segment-individual-led-control
    # TODO: split big calls up into multiple smaller ones
    _set_state({"seg": {"i": compress(colors)}})


def set_leds_sparse(colors: dict[int, RGBColor]) -> None:
    """Changes the colors of the specified LEDs only."""
    leds: list[str | int] = []
    for pos, color in colors.items():
        leds.append(pos)
        leds.append(str(color))
    _set_state({"seg": {"i": leds}})


def compress(colors: Iterable[RGBColor]) -> list[str | int]:
    offset = 0
    compressed: list[str | int] = []
    for color, size in run_length.encode(colors):
        color_hex = str(color)
        if size == 1:
            compressed.append(color_hex)
        else:
            compressed.extend([offset, offset + size, color_hex])
        offset += size

    return compressed


def main() -> None:
    # cycle_rainbow()
    chase()

    # colors = {5: OFF, 8: RGBColor(255, 255, 255), 9: RGBColor(0, 255, 0), 10: RGBColor(255, 0, 0), 1: OFF}
    # set_leds_sparse(colors)


def chase() -> None:
    last = time.perf_counter_ns()
    for i in itertools.cycle(range(NUM_LEDS)):
        if i == 0:
            now = time.perf_counter_ns()
            fps = 360 / ((now - last) / 1_000_000_000)
            print(f"{fps:.2f} fps")
            last = now
        values = [OFF] * NUM_LEDS
        values[(i - 2) % NUM_LEDS] = RGBColor(64, 64, 64)
        values[(i - 1) % NUM_LEDS] = RGBColor(128, 128, 128)
        values[i] = RGBColor(255, 255, 255)
        values[(i + 1) % NUM_LEDS] = RGBColor(128, 128, 128)
        values[(i + 2) % NUM_LEDS] = RGBColor(64, 64, 64)
        set_leds_all(values)


def cycle_rainbow(cycle_length: int = 100) -> None:
    last = time.perf_counter_ns()
    for h in itertools.cycle(range(cycle_length)):
        if h == cycle_length - 1:
            now = time.perf_counter_ns()
            fps = cycle_length / ((now - last) / 1_000_000_000)
            print(f"{fps:.2f} fps")
            last = now
        values = [
            RGBColor.from_hsv(hue=((h + i) % cycle_length) / cycle_length, sat=1, val=1)
            for i in range(NUM_LEDS)
        ]
        set_leds_all(values)


if __name__ == "__main__":
    main()
