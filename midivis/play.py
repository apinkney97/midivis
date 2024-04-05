import asyncio
import pathlib
import subprocess
import time
from contextlib import contextmanager
from typing import AsyncIterator, Iterable

import mido
from rich.live import Live

from midivis.display import Display
from midivis.utils import get_console, log


# class Player:
#     def __init__(self):
#         pass
#
#     async def play(self):
#         pass
#
#     async def pause(self):
#         pass
#
#     async def skip(self, seconds: float = 10):
#         pass
#
#     # Playlist management
#
#     async def add_track(self, track: Track):
#         pass
#
#     async def remove_track(self, playlist_id: int):
#         pass
#
#     async def bump_track_up(self, playlist_id: int):
#         pass
#
#     async def bump_track_down(self, playlist_id: int):
#         pass
#
#
async def play_async(
    midi_file: mido.MidiFile,
    meta_messages: bool = False,
    start_secs: float = 0.0,
    synth_port=None,
) -> AsyncIterator[tuple[list[mido.Message | mido.MetaMessage], float]]:
    """
    Async generator that yields MIDI messages in real time.

    This is similar to `MidiFile.play()`, except that it:
        - uses async sleeps instead of blocking ones
        - groups simultaneous messages together
    """

    abs_start_time = time.monotonic() - start_secs
    progress_secs = 0.0

    message_group = []

    for message in midi_file:
        want_message = True

        if isinstance(message, mido.MetaMessage) and not meta_messages:
            want_message = False

        if progress_secs < start_secs and message.type in {"note_on", "note_off"}:
            # Skip note on/off messages before we start. Note that
            # we must not skip other messages since they may have
            # side-effects, eg `program_change`. This does mean
            # that any notes whose `note_off` has not yet occurred
            # at `start_secs` will not be sounding.
            want_message = False

        if message.time > 0:
            # yield the previous group (if nonempty)
            if message_group:
                yield message_group, progress_secs

            # start a new group with the message
            message_group = [message] if want_message else []

            # sleep until the message should be played
            progress_secs += message.time

            playback_time = time.monotonic() - abs_start_time
            seconds_to_next_event = progress_secs - playback_time

            if seconds_to_next_event > 0:
                await asyncio.sleep(seconds_to_next_event)

        elif want_message:
            # message has time 0; append it to the existing group
            message_group.append(message)

        if want_message and synth_port is not None:
            synth_port.send(message)

    # yield any final group:
    if message_group:
        yield message_group, progress_secs


@contextmanager
def port():
    mido.set_backend("mido.backends.rtmidi/LINUX_ALSA")
    timidity_handle = None
    try:
        synth_port = mido.open_output("TiMidity port 0")
    except OSError:
        # Attempt to start timidity if it's not running
        timidity_handle = subprocess.Popen(["timidity", "-iAD"])
        timidity_handle.wait()
        time.sleep(1)
        synth_port = mido.open_output("TiMidity port 0")

    try:
        yield synth_port
    finally:
        synth_port.close()

        # Stop timidity if we started it
        if timidity_handle is not None:
            timidity_handle.terminate()


async def play(synth_port, midi_path: pathlib.Path, start_secs: float = 0.0) -> None:
    mf = mido.MidiFile(filename=midi_path, clip=True)

    display = Display(
        title=str(midi_path), duration_secs=mf.length, progress_secs=start_secs
    )

    with Live(console=get_console(), auto_refresh=False) as live:
        async for messages, progress_secs in play_async(
            mf, start_secs=start_secs, synth_port=synth_port
        ):
            # TODO: Consider splitting out "play" into its own thread/process

            for message in messages:
                display.update(message, progress_secs)

            if display.needs_redraw:
                live.update(display.to_panel(with_instruments=False), refresh=True)

        # Clear the screen at the end
        live.update("", refresh=True)


def play_many(paths: Iterable[pathlib.Path]) -> None:
    asyncio.run(_play_many(paths))


async def _play_many(paths: Iterable[pathlib.Path]) -> None:
    with port() as synth_port:
        for path in paths:
            try:
                await play(synth_port, path)
            except Exception as e:
                log(0, f"{type(e).__name__}: {e}")
                raise


# Good ones:
# Music/The_Magic_of_MIDI/MIDI/00920SZ3.MID
# Music/The_Magic_of_MIDI/MIDI/00930SZ4.MID
