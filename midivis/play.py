import asyncio
import colorsys
import pathlib
import time
from contextlib import contextmanager
from datetime import timedelta
from itertools import islice
from typing import AsyncIterator, Iterable

import mido
from rich import print
from rich.color import Color
from rich.live import Live
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from midivis.midi_metadata import (
    CONTROL_CHANGE,
    NOTES_PER_CHANNEL,
    NUM_CHANNELS,
    PERCUSSION_CHANNEL,
    PROGRAMS,
)

LOW_LIMIT = 16
HIGH_LIMIT = LOW_LIMIT + 100

# DEBUG = True
DEBUG = False


def color_from_hsv(hue: float, saturation: float, value):
    r, g, b = (x * 255 for x in colorsys.hsv_to_rgb(hue, saturation, value))
    return Color.from_rgb(r, g, b)


class AsyncMidiFile(mido.MidiFile):
    async def play_async(
        self, meta_messages: bool = False, start_secs: float = 0.0
    ) -> AsyncIterator[tuple[mido.Message, float]]:
        """
        Async generator that yields MIDI messages in real time.

        This is brodly equivalent to `play()` on the superclass,
        but uses async sleeps instead of blocking ones.
        """

        start_time = time.monotonic() - start_secs
        progress_secs = 0.0

        for message in self:
            progress_secs += message.time

            playback_time = time.monotonic() - start_time
            seconds_to_next_event = progress_secs - playback_time

            if seconds_to_next_event > 0:
                await asyncio.sleep(seconds_to_next_event)

            if isinstance(message, mido.MetaMessage) and not meta_messages:
                continue

            if progress_secs < start_secs and message.type in {"note_on", "note_off"}:
                # Skip note on/off messages before we start. Note that
                # we must not skip other messages since they # may have
                # side-effects, eg `program_change`. This does mean
                # that any notes whose `note_off` has not yet occurred
                # at `start_secs` will not be sounding.
                continue

            yield message, progress_secs


@contextmanager
def port():
    mido.set_backend("mido.backends.rtmidi/LINUX_ALSA")
    output = mido.open_output("TiMidity port 0")
    try:
        yield output
    finally:
        output.close()


def init_midi():
    pass


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


async def play(output, midi_path: pathlib.Path, start_secs: float = 0.0) -> None:
    mf = AsyncMidiFile(midi_path, clip=True)

    duration = mf.length
    channels = [bytearray(NOTES_PER_CHANNEL) for _ in range(NUM_CHANNELS)]
    instruments = [0] * NUM_CHANNELS

    with Live(
        render_channel_data(
            channels, instruments, str(midi_path), start_secs, duration
        ),
        auto_refresh=False,
    ) as live:
        needs_rerender = False
        async for message, progress_secs in mf.play_async(start_secs=start_secs):
            match message.type:
                case "note_on":
                    channels[message.channel][message.note] = message.velocity
                    needs_rerender = True
                case "note_off":
                    channels[message.channel][message.note] = 0
                    needs_rerender = True
                case "program_change":
                    instruments[message.channel] = message.program
                    debug(
                        f"PROGRAM: channel={message.channel} voice={PROGRAMS[message.program + 1]!r}"
                    )
                case "control_change":
                    function = CONTROL_CHANGE.get(message.control, "Unknown")
                    debug(
                        f"CONTROL: {function!r} channel={message.channel} value={message.value}"
                    )
                case _:
                    debug(message)

            output.send(message)

            if message.time > 0 and needs_rerender:
                live.update(
                    render_channel_data(
                        channels, instruments, str(midi_path), progress_secs, duration
                    )
                )
                live.refresh()
                needs_rerender = False


def render_channel_data(
    channels: list[bytearray],
    instruments: list[int],
    title: str,
    pos: float,
    duration: float,
) -> Panel:
    text = Text()

    for channel_num, channel in enumerate(channels, start=1):
        instrument = instruments[channel_num - 1]
        hue = instrument / 127  # Colour by instrument
        sat = 0 if channel_num == PERCUSSION_CHANNEL else 1  # Make percussion white

        notes = []
        max_val = 0
        for velocity in islice(channel, LOW_LIMIT, HIGH_LIMIT):
            if velocity:
                val = velocity / 127  # louder => brighter
                max_val = max(max_val, val)
                style = Style(color=color_from_hsv(hue, sat, val))
                notes.append(Text("\u25ae", style=style))
            else:
                notes.append("\u25af")

        instrument_name = (
            "Percussion"
            if channel_num == PERCUSSION_CHANNEL
            else PROGRAMS[instrument + 1]
        )
        text.append(f"Track {channel_num:02d}: ")
        text.append(
            instrument_name,
            style=Style(color=color_from_hsv(hue, sat, max(0.2, max_val))),
        )
        text.append("\n")

        for note in notes:
            text.append(note)

        text.append("\n")

    text.remove_suffix("\n")

    duration_td = timedelta(seconds=int(duration))
    pos_td = timedelta(seconds=int(pos))

    return Panel.fit(
        text,
        title=f"[white]{title}[/white]",
        subtitle=f"[white]{pos_td} / {duration_td}[/white]",
        subtitle_align="right",
        style=Style(bgcolor=Color.from_rgb(0, 0, 0), color=Color.from_rgb(32, 32, 32)),
    )


# async def main():
#     files = sys.argv[1:]
#     if not files:
#         files = ["Music/MUSICS/MONTAGUE.MID"]
#
#     await _play_many(files)


def play_many(paths: Iterable[pathlib.Path]) -> None:
    asyncio.run(_play_many(paths))


async def _play_many(paths: Iterable[pathlib.Path]) -> None:
    with port() as output:
        for path in paths:
            try:
                await play(output, path)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                raise


# if __name__ == "__main__":
#     asyncio.run(main())

# Good ones:
# Music/The_Magic_of_MIDI/MIDI/00920SZ3.MID
# Music/The_Magic_of_MIDI/MIDI/00930SZ4.MID
