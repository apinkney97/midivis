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


class AsyncMidiFile(mido.MidiFile):
    async def play_async(
        self, meta_messages: bool = False, start_secs: float = 0.0
    ) -> AsyncIterator[tuple[mido.Message | mido.MetaMessage, float]]:
        """
        Async generator that yields MIDI messages in real time.

        This is brodly equivalent to `play()` on the superclass,
        but uses async sleeps instead of blocking ones.
        """

        # TODO: Group simultaneous messages

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
                # we must not skip other messages since they may have
                # side-effects, eg `program_change`. This does mean
                # that any notes whose `note_off` has not yet occurred
                # at `start_secs` will not be sounding.
                continue

            yield message, progress_secs


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
    mf = AsyncMidiFile(midi_path, clip=True)

    display = Display(
        title=str(midi_path), duration_secs=mf.length, progress_secs=start_secs
    )

    with Live(console=get_console(), auto_refresh=False) as live:
        async for message, progress_secs in mf.play_async(start_secs=start_secs):
            synth_port.send(message)
            needs_redraw = display.update(message, progress_secs)

            if needs_redraw:
                live.update(display.render_channel_data())
                live.refresh()

        live.update("")
        live.refresh()


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
