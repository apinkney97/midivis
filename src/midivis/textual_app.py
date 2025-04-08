from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Placeholder, Static

# Useful: https://en.wikipedia.org/wiki/Media_control_symbols
PLAY_ICON = "\u23f5"
PAUSE_ICON = "\u23f8"
NEXT_ICON = "\u23ed"
PREV_ICON = "\u23ee"


class PlayingTrackInfo(Static):
    pass


class Controls(Static):
    def compose(self) -> ComposeResult:
        yield Button(PREV_ICON, id="prev")
        yield Button(PLAY_ICON, id="play")
        yield Button(PAUSE_ICON, id="pause")
        yield Button(NEXT_ICON, id="next")
        yield Placeholder("Progress bar")


class TrackInfo(Static):
    def compose(self) -> ComposeResult:
        yield VoiceInfo()
        yield NotesContainer()


class VoiceInfo(Static):
    def compose(self) -> ComposeResult:
        yield Placeholder("\n".join(f"voice {n + 1}" for n in range(16)))


class NotesContainer(Static):  # TODO: Consider using HorizontalScroll
    def compose(self) -> ComposeResult:
        yield Placeholder("\n".join(f"track {n + 1}" for n in range(16)))


class PlaylistManager(Static):
    def compose(self) -> ComposeResult:
        yield SearchWidget()
        yield Placeholder("Playlist add/remove/up/down buttons", id="playlist_buttons")
        yield Placeholder("Playlist", id="playlist")


class SearchWidget(Static):
    def compose(self) -> ComposeResult:
        yield Placeholder("search box", id="search_box")
        yield Placeholder("search results table", id="search_results_table")


class MidiVisApp(App[int]):
    CSS_PATH = "midivis.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield PlayingTrackInfo("No track playing")
        yield Controls()
        yield TrackInfo()
        yield PlaylistManager()


if __name__ == "__main__":
    app = MidiVisApp()
    app.run()
