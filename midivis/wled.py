"""
Helpers to call the WLED API
"""

import functools
import itertools
import time
from typing import NamedTuple

import requests
from more_itertools import run_length

HOST = "192.168.1.205"
NUM_LEDS = 256


class RGBColor(NamedTuple):
    # Values must be 0-255
    r: int
    g: int
    b: int

    def __str__(self):
        return f"{self.r:02X}{self.g:02X}{self.b:02X}"


def set_state(data: dict) -> None:
    resp = requests.post(f"http://{HOST}/json/state", json=data)
    resp.raise_for_status()


def set_leds(colors: list[RGBColor | int]) -> None:
    set_state({"seg": {"i": compress(colors)}})


def compress(colors: list[RGBColor]) -> list[RGBColor | int]:
    offset = 0
    compressed = []
    for color, size in run_length.encode(colors):
        if size == 1:
            compressed.append(color)
        else:
            compressed.extend([offset, offset + size, color])
        offset += size

    # print(colors)
    # print(compressed)
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


def chase():
    last = time.perf_counter_ns()
    for i in itertools.cycle(range(NUM_LEDS)):
        if i == 0:
            now = time.perf_counter_ns()
            fps = 360 / ((now - last) / 1_000_000_000)
            print(f"{fps:.2f} fps")
            last = now
        values = [RGBColor(0, 0, 0)] * NUM_LEDS
        values[(i - 2) % NUM_LEDS] = RGBColor(64, 64, 64)
        values[(i - 1) % NUM_LEDS] = RGBColor(128, 128, 128)
        values[i] = RGBColor(255, 255, 255)
        values[(i + 1) % NUM_LEDS] = RGBColor(128, 128, 128)
        values[(i + 2) % NUM_LEDS] = RGBColor(64, 64, 64)
        set_leds(values)


def cycle_rainbow():
    last = time.perf_counter_ns()
    for h in itertools.cycle(range(360)):
        if h == 359:
            now = time.perf_counter_ns()
            fps = 360 / ((now - last) / 1_000_000_000)
            print(f"{fps:.2f} fps")
            last = now
        values = [hsv_to_rgb((h + i) % 360, 1, 1) for i in range(NUM_LEDS)]
        set_leds(values)


if __name__ == "__main__":
    main()
