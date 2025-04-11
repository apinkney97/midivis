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
)
from midivis.wled import OFF, RGBColor


def color_from_hsv(hue: float, saturation: float, value: float) -> Color:
    r, g, b = (x * 255 for x in colorsys.hsv_to_rgb(hue, saturation, value))
    return Color.from_rgb(r, g, b)


FILLED_RECTANGLE = "\u25ae"
EMPTY_RECTANGLE = "\u25af"
FILLED_CIRCLE = "\u25cf"
EMPTY_CIRCLE = "\u25cb"


@dataclass
class Channel:
    """
    Maintains the current state of a single MIDI channel
    """

    num: int

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
    ) -> None:
        self._title = title
        self._duration_secs = duration_secs
        self._progress_secs = progress_secs
        self._channels = [Channel(num=i + 1) for i in range(NUM_CHANNELS)]

        self._needs_redraw = False

        self._colors = [[OFF] * NOTES_PER_CHANNEL for _ in range(NUM_CHANNELS)]

    @property
    def title(self) -> str:
        return self._title

    @property
    def duration_secs(self) -> float:
        return self._duration_secs

    @property
    def progress_secs(self) -> float:
        return self._progress_secs

    @property
    def needs_redraw(self) -> bool:
        return self._needs_redraw

    @property
    def colors(self) -> list[list[RGBColor]]:
        return self._colors

    def update(self, message: Message, progress_secs: float) -> None:
        """
        Updates the internal state with the given MIDI message.
        """
        self._progress_secs = progress_secs
        match message.type:
            case "note_on":
                channel = self._channels[message.channel]
                channel.velocities[message.note] = message.velocity
                self.set_note_color(channel, message.note)

            case "note_off":
                channel = self._channels[message.channel]
                channel.velocities[message.note] = 0
                self.set_note_color(channel, message.note)

            case "program_change":
                channel = self._channels[message.channel]
                channel.program = message.program
                self.recolor_channel(channel)

            case "control_change":
                channel = self._channels[message.channel]
                match message.control:
                    case 7:
                        channel.volume = message.value
                        self.recolor_channel(channel)

    def recolor_channel(self, channel: Channel) -> None:
        for note in range(NOTES_PER_CHANNEL):
            self.set_note_color(channel, note)

    def set_note_color(self, channel: Channel, note: int) -> None:
        old_color = self._colors[channel.num - 1][note]

        velocity = channel.velocities[note]
        if channel.volume == 0 or velocity == 0:
            new_color = OFF

        else:
            hue = channel.program / 0x7F  # Colour by instrument
            sat = 0 if channel.num == PERCUSSION_CHANNEL else 1  # Make percussion white

            volume_fraction = channel.volume / 0x7F
            val = velocity / 0x7F * volume_fraction  # louder => brighter

            new_color = RGBColor.from_hsv(hue, sat, val)

        if new_color != old_color:
            self._colors[channel.num - 1][note] = new_color
            self._needs_redraw = True


def to_panel(
    display: Display,
    with_instruments: bool = True,
    lower_limit: int = 0,
    note_range: int = 100,
) -> Panel:
    """
    Returns a rich Panel representing the currently playing notes.
    """
    lower_limit = max(0, lower_limit)
    upper_limit = min(NOTES_PER_CHANNEL, lower_limit + note_range)

    text = Text()

    for channel_num, colors in enumerate(display.colors, start=1):
        notes: list[Text | str] = []

        for color in islice(colors, lower_limit, upper_limit):
            if color is not OFF:
                style = Style(color=Color.from_rgb(*color))
                notes.append(Text(FILLED_RECTANGLE, style=style))
            else:
                notes.append(EMPTY_RECTANGLE)
                # notes.append(" ")

        # TODO: fix this
        # if with_instruments:
        #     instrument_name = (
        #         "Percussion"
        #         if channel_num == PERCUSSION_CHANNEL
        #         else PROGRAMS[channel.program + 1]
        #     )
        #     # text.append(f"Track {channel_num:02d}: ")
        #     text.append(
        #         f"vol:0x{channel.volume:02x}     {instrument_name}",
        #         style=Style(color=color_from_hsv(hue, sat, max(0.2, max_val))),
        #     )
        #     text.append("\n")

        for note in notes:
            text.append(note)

        text.append("\n")

    text.remove_suffix("\n")

    duration_td = timedelta(seconds=int(display.duration_secs))
    pos_td = timedelta(seconds=int(display.progress_secs))

    return Panel.fit(
        text,
        title=f"[white]{display.title}[/white]",
        subtitle=f"[white]{pos_td} / {duration_td}[/white]",
        subtitle_align="right",
        style=Style(bgcolor=Color.from_rgb(0, 0, 0), color=Color.from_rgb(32, 32, 32)),
    )
