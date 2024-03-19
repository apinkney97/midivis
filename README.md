# `midivis`: a MIDI Visualiser

Note: this is still a work in progress.

Provides a live visualisation of MIDI playback in the terminal, and optionally pushes the visualisation to addressible LEDs using [WLED](https://kno.wled.ge/)'s [JSON API](https://kno.wled.ge/interfaces/json-api/).

## Background

Visualising the playback of MIDI files like this is not a new idea. I saw a tweet sometime during a COVID-19 lockdown (I think late 2020 or early 2021) where someone had created a visualisation for the infamous [canyon.mid](https://archive.org/details/canyon_202011) that shipped with Windows 98.

Other programs that exist that perform roughly the same function include [DosMid](https://dosmid.sourceforge.net/) and [TiMidity++](https://timidity.sourceforge.net/) (run using the `-int` option).

So far as I know there is no other program that pushes MIDI visualisations to addressible LEDs, so I thought I'd write one. And in any case it sounded like a fun challenge!

## Running

Note: I have only tested this on Ubuntu and Raspberry Pi OS.

### First time setup
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Install this project's requirements:
   ```shell
   poetry install
   ```
3. Install [TiMidity++](https://en.wikipedia.org/wiki/TiMidity%2B%2B):
   ```shell
   sudo apt install timidity
   ```

### Visualising a MIDI file

1. Ensure TiMidity++ is running with the ALSA sequencer interface:
   ```shell
   timidity -iA
   ```
2. Use `midivis play` to play your file(s) in the terminal:
   ```shell
   poetry run midivis play <path-to-midi> [<path-to-more-midis>]
   ```

## Useful links

### MIDI collections
- [The Magic of MIDI](https://archive.org/details/themagicofmidiv1)

### Sound fonts
- [500 Soundfonts Collection - Full GM Sets, SF2 Pack](https://archive.org/details/500-soundfonts-full-gm-sets)


## TODO:
- Replace play.py with a [textual](https://github.com/Textualize/textual) UI (currently WIP)
- Decouple terminal UI from MIDI playback to support multiple simultaneous outputs (terminal, WLED, MIDI synthesizer).
