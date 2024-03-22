import colorsys
from dataclasses import dataclass, field
from datetime import timedelta
from itertools import islice

from mido import Message
from rich.color import Color
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from midivis.midi_metadata import (
    NOTES_PER_CHANNEL,
    NUM_CHANNELS,
    PERCUSSION_CHANNEL,
    PROGRAMS,
)
from midivis.utils import log


def color_from_hsv(hue: float, saturation: float, value):
    r, g, b = (x * 255 for x in colorsys.hsv_to_rgb(hue, saturation, value))
    return Color.from_rgb(r, g, b)


@dataclass
class Channel:
    """
    Maintains the current state of a single MIDI channel
    """

    # Current instrument/voice
    program: int = 0

    # Current volume. TODO: check if 100 is actually the default.
    volume: int = 100

    # Notes and how loudly they are playing
    velocities: bytearray = field(default_factory=lambda: bytearray(NOTES_PER_CHANNEL))


class Display:
    """
    Tracks the current display state.

    Ingests MIDI messages and applies relevant changes.
    """

    def __init__(
        self,
        title: str,
        duration_secs: float,
        progress_secs: float = 0.0,
        lower_limit: int = 16,
        note_range: int = 100,
    ):
        self.title = title
        self.duration_secs = duration_secs
        self.progress_secs = progress_secs
        self.channels = [Channel() for _ in range(NUM_CHANNELS)]

        self.needs_redraw = False
        self.lower_limit = lower_limit
        self.upper_limit = lower_limit + note_range

    def update(self, message: Message, progress_secs: float) -> bool:
        """
        Returns True if the display needs to be updated, False otherwise.
        """
        self.progress_secs = progress_secs
        match message.type:
            case "note_on":
                channel = self.channels[message.channel]
                channel.velocities[message.note] = message.velocity
                self.needs_redraw = True
            case "note_off":
                channel = self.channels[message.channel]
                channel.velocities[message.note] = 0
                self.needs_redraw = True
            case "program_change":
                channel = self.channels[message.channel]
                channel.program = message.program
            case "control_change":
                channel = self.channels[message.channel]
                if message.control == 7:
                    channel.volume = message.value
            case _:
                log(1, message)

        # This is probably wrong, as only the first of simultaneous changes will be applied.
        # Really we need to batch simultaneous messages...
        needs_redraw = self.needs_redraw and message.time > 0
        return needs_redraw

    def render_channel_data(self) -> Panel:
        """
        Returns a rich Panel representing the currently playing notes.
        """
        text = Text()

        for channel_num, channel in enumerate(self.channels, start=1):
            hue = channel.program / 127  # Colour by instrument
            sat = 0 if channel_num == PERCUSSION_CHANNEL else 1  # Make percussion white

            notes = []
            max_val = 0
            volume_fraction = channel.volume / 0x7F

            for velocity in islice(
                channel.velocities, self.lower_limit, self.upper_limit
            ):
                if velocity:
                    val = velocity / 127 * volume_fraction  # louder => brighter
                    max_val = max(max_val, val)
                    style = Style(color=color_from_hsv(hue, sat, val))
                    notes.append(Text("\u25ae", style=style))
                else:
                    notes.append("\u25af")

            instrument_name = (
                "Percussion"
                if channel_num == PERCUSSION_CHANNEL
                else PROGRAMS[channel.program + 1]
            )
            # text.append(f"Track {channel_num:02d}: ")
            text.append(
                f"vol:0x{channel.volume:02x}     {instrument_name}",
                style=Style(color=color_from_hsv(hue, sat, max(0.2, max_val))),
            )
            text.append("\n")

            for note in notes:
                text.append(note)

            text.append("\n")

        text.remove_suffix("\n")

        duration_td = timedelta(seconds=int(self.duration_secs))
        pos_td = timedelta(seconds=int(self.progress_secs))

        return Panel.fit(
            text,
            title=f"[white]{self.title}[/white]",
            subtitle=f"[white]{pos_td} / {duration_td}[/white]",
            subtitle_align="right",
            style=Style(
                bgcolor=Color.from_rgb(0, 0, 0), color=Color.from_rgb(32, 32, 32)
            ),
        )
