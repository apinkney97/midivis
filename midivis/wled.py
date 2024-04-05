"""
Helpers to call the WLED API
"""

import colorsys
import functools
import itertools
import time
from typing import NamedTuple

from more_itertools import run_length
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

HOST = "192.168.1.149"
LEDS_WIDTH = 100
LEDS_HEIGHT = 16
NUM_LEDS = LEDS_WIDTH * LEDS_HEIGHT


class RGBColor(NamedTuple):
    # Values must be 0-255
    r: int
    g: int
    b: int

    def __str__(self):
        return f"{self.r:02X}{self.g:02X}{self.b:02X}"

    @classmethod
    def from_hsv(cls, hue: float, sat: float, val: float) -> "RGBColor":
        # h/s/v in range 0-1
        r, g, b = (int(x * 255) for x in colorsys.hsv_to_rgb(hue, sat, val))
        return cls(r, g, b)


OFF = RGBColor(0, 0, 0)

s = Session()
retries = Retry(
    total=3,
    backoff_factor=0.1,
    status_forcelist=[502, 503, 504],
    allowed_methods={"POST"},
)
s.mount("http://", HTTPAdapter(max_retries=retries))


def _set_state(data: dict) -> None:
    """Raw call to /json/state on the WLED API."""
    # import json; print(json.dumps(data)); return
    resp = s.post(f"http://{HOST}/json/state", json=data)
    resp.raise_for_status()


def set_leds_all(colors: list[RGBColor]) -> None:
    """Sets the LEDs to the specified colors."""
    # See https://kno.wled.ge/interfaces/json-api/#per-segment-individual-led-control
    _set_state({"seg": {"i": compress(colors)}})


def set_leds_sparse(colors: dict[int, RGBColor]) -> None:
    """Changes the colors of the specified LEDs only."""
    leds = []
    for pos, color in colors.items():
        leds.append(pos)
        leds.append(str(color))
    _set_state({"seg": {"i": leds}})


def compress(colors: list[RGBColor]) -> list[str | int]:
    offset = 0
    compressed = []
    for color, size in run_length.encode(colors):
        color_hex = str(color)
        if size == 1:
            compressed.append(color_hex)
        else:
            compressed.extend([offset, offset + size, color_hex])
        offset += size

    return compressed


@functools.cache
def hsv_to_rgb(h: float, s: float, v: float) -> RGBColor:
    # h: 0 - 360
    # s: 0 - 1
    # v: 0 - 1
    # returns: RGBColor(r, g, b) values 0-255
    def f(n):
        k = (n + h / 60) % 6
        return int(255 * (v - v * s * max(0, min(k, 4 - k, 1))))

    return RGBColor(r=f(5), g=f(3), b=f(1))


def main():
    # cycle_rainbow()
    chase()

    # colors = {5: OFF, 8: RGBColor(255, 255, 255), 9: RGBColor(0, 255, 0), 10: RGBColor(255, 0, 0), 1: OFF}
    # set_leds_sparse(colors)


def chase():
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


def cycle_rainbow():
    last = time.perf_counter_ns()
    for h in itertools.cycle(range(360)):
        if h == 359:
            now = time.perf_counter_ns()
            fps = 360 / ((now - last) / 1_000_000_000)
            print(f"{fps:.2f} fps")
            last = now
        values = [hsv_to_rgb((h + i) % 360, 1, 1) for i in range(NUM_LEDS)]
        set_leds_all(values)


if __name__ == "__main__":
    main()
