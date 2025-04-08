"""
Useful metadata regarding the MIDI spec
"""

# TODO: Look into replacing with https://github.com/EMATech/midi_const/

NUM_CHANNELS = 16
NOTES_PER_CHANNEL = 128
PERCUSSION_CHANNEL = 10


# From: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
CONTROL_CHANGE = {
    0: "Bank Select",  # 0-127",  # MSB
    1: "Modulation Wheel or Lever",  # 0-127",  # MSB
    2: "Breath Controller",  # 0-127",  # MSB
    4: "Foot Controller",  # 0-127",  # MSB
    5: "Portamento Time",  # 0-127",  # MSB
    6: "Data Entry MSB",  # 0-127",  # MSB
    7: "Channel Volume (formerly Main Volume)",  # 0-127",  # MSB
    8: "Balance",  # 0-127",  # MSB
    10: "Pan",  # 0-127",  # MSB
    11: "Expression Controller",  # 0-127",  # MSB
    12: "Effect Control 1",  # 0-127",  # MSB
    13: "Effect Control 2",  # 0-127",  # MSB
    16: "General Purpose Controller 1",  # 0-127",  # MSB
    17: "General Purpose Controller 2",  # 0-127",  # MSB
    18: "General Purpose Controller 3",  # 0-127",  # MSB
    19: "General Purpose Controller 4",  # 0-127",  # MSB
    32: "LSB for Control 0 (Bank Select)",  # 0-127",  # LSB
    33: "LSB for Control 1 (Modulation Wheel or Lever)",  # 0-127",  # LSB
    34: "LSB for Control 2 (Breath Controller)",  # 0-127",  # LSB
    35: "LSB for Control 3 (Undefined)",  # 0-127",  # LSB
    36: "LSB for Control 4 (Foot Controller)",  # 0-127",  # LSB
    37: "LSB for Control 5 (Portamento Time)",  # 0-127",  # LSB
    38: "LSB for Control 6 (Data Entry)",  # 0-127",  # LSB
    39: "LSB for Control 7 (Channel Volume, formerly Main Volume)",  # 0-127",  # LSB
    40: "LSB for Control 8 (Balance)",  # 0-127",  # LSB
    41: "LSB for Control 9 (Undefined)",  # 0-127",  # LSB
    42: "LSB for Control 10 (Pan)",  # 0-127",  # LSB
    43: "LSB for Control 11 (Expression Controller)",  # 0-127",  # LSB
    44: "LSB for Control 12 (Effect control 1)",  # 0-127",  # LSB
    45: "LSB for Control 13 (Effect control 2)",  # 0-127",  # LSB
    46: "LSB for Control 14 (Undefined)",  # 0-127",  # LSB
    47: "LSB for Control 15 (Undefined)",  # 0-127",  # LSB
    48: "LSB for Control 16 (General Purpose Controller 1)",  # 0-127",  # LSB
    49: "LSB for Control 17 (General Purpose Controller 2)",  # 0-127",  # LSB
    50: "LSB for Control 18 (General Purpose Controller 3)",  # 0-127",  # LSB
    51: "LSB for Control 19 (General Purpose Controller 4)",  # 0-127",  # LSB
    52: "LSB for Control 20 (Undefined)",  # 0-127",  # LSB
    53: "LSB for Control 21 (Undefined)",  # 0-127",  # LSB
    54: "LSB for Control 22 (Undefined)",  # 0-127",  # LSB
    55: "LSB for Control 23 (Undefined)",  # 0-127",  # LSB
    56: "LSB for Control 24 (Undefined)",  # 0-127",  # LSB
    57: "LSB for Control 25 (Undefined)",  # 0-127",  # LSB
    58: "LSB for Control 26 (Undefined)",  # 0-127",  # LSB
    59: "LSB for Control 27 (Undefined)",  # 0-127",  # LSB
    60: "LSB for Control 28 (Undefined)",  # 0-127",  # LSB
    61: "LSB for Control 29 (Undefined)",  # 0-127",  # LSB
    62: "LSB for Control 30 (Undefined)",  # 0-127",  # LSB
    63: "LSB for Control 31 (Undefined)",  # 0-127",  # LSB
    64: "Damper Pedal on/off (Sustain)",  # ≤63 off, ≥64 on",  # ---
    65: "Portamento On/Off",  # ≤63 off, ≥64 on",  # ---
    66: "Sostenuto On/Off",  # ≤63 off, ≥64 on",  # ---
    67: "Soft Pedal On/Off",  # ≤63 off, ≥64 on",  # ---
    68: "Legato Footswitch",  # ≤63 Normal, ≥64 Legato",  # ---
    69: "Hold 2",  # ≤63 off, ≥64 on",  # ---
    70: "Sound Controller 1 (default: Sound Variation)",  # 0-127",  # LSB
    71: "Sound Controller 2 (default: Timbre/Harmonic Intens.)",  # 0-127",  # LSB
    72: "Sound Controller 3 (default: Release Time)",  # 0-127",  # LSB
    73: "Sound Controller 4 (default: Attack Time)",  # 0-127",  # LSB
    74: "Sound Controller 5 (default: Brightness)",  # 0-127",  # LSB
    75: "Sound Controller 6 (default: Decay Time - see MMA RP-021)",  # 0-127",  # LSB
    76: "Sound Controller 7 (default: Vibrato Rate - see MMA RP-021)",  # 0-127",  # LSB
    77: "Sound Controller 8 (default: Vibrato Depth - see MMA RP-021)",  # 0-127",  # LSB
    78: "Sound Controller 9 (default: Vibrato Delay - see MMA RP-021)",  # 0-127",  # LSB
    79: "Sound Controller 10 (default undefined - see MMA RP-021)",  # 0-127",  # LSB
    80: "General Purpose Controller 5",  # 0-127",  # LSB
    81: "General Purpose Controller 6",  # 0-127",  # LSB
    82: "General Purpose Controller 7",  # 0-127",  # LSB
    83: "General Purpose Controller 8",  # 0-127",  # LSB
    84: "Portamento Control",  # 0-127",  # LSB
    88: "High Resolution Velocity Prefix",  # 0-127",  # LSB
    91: "Effects 1 Depth",  # 0-127",  # ---
    92: "Effects 2 Depth (formerly Tremolo Depth)",  # 0-127",  # ---
    93: "Effects 3 Depth",  # 0-127",  # ---
    94: "Effects 4 Depth (formerly Celeste [Detune] Depth)",  # 0-127",  # ---
    95: "Effects 5 Depth (formerly Phaser Depth)",  # 0-127",  # ---
    96: "Data Increment (Data Entry +1) (see MMA RP-018)",  # N/A",  # ---
    97: "Data Decrement (Data Entry -1) (see MMA RP-018)",  # N/A",  # ---
    98: "Non-Registered Parameter Number (NRPN) - LSB",  # 0-127",  # LSB
    99: "Non-Registered Parameter Number (NRPN) - MSB",  # 0-127",  # MSB
    100: "Registered Parameter Number (RPN) - LSB*",  # 0-127",  # LSB
    101: "Registered Parameter Number (RPN) - MSB*",  # 0-127",  # MSB
    120: "[Channel Mode Message] All Sound Off",  # 0",  # ---
    121: "[Channel Mode Message] Reset All Controllers",  # 0",  # ---
    122: "[Channel Mode Message] Local Control On/Off",  # 0 off, 127 on",  # ---
    123: "[Channel Mode Message] All Notes Off",  # 0",  # ---
    124: "[Channel Mode Message] Omni Mode Off (+ all notes off)",  # 0",  # ---
    125: "[Channel Mode Message] Omni Mode On (+ all notes off)",  # 0",  # ---
    126: "[Channel Mode Message] Mono Mode On (+ poly off, + all notes off)",  #
    127: "[Channel Mode Message] Poly Mode On (+ mono off, +all notes off)",  # 0",  # ---
}

# source: https://en.wikipedia.org/wiki/General_MIDI
PROGRAMS = {
    # Piano
    1: "Acoustic Grand Piano",
    2: "Bright Acoustic Piano",
    3: "Electric Grand Piano",
    4: "Honky-tonk Piano",
    5: "Electric Piano 1 (usually a Rhodes Piano)",
    6: "Electric Piano 2 (usually an FM piano patch)",
    7: "Harpsichord",
    8: "Clavinet",
    # Chromatic Percussion
    9: "Celesta",
    10: "Glockenspiel",
    11: "Music Box",
    12: "Vibraphone",
    13: "Marimba",
    14: "Xylophone",
    15: "Tubular Bells",
    16: "Dulcimer",
    # Organ
    17: "Drawbar Organ",
    18: "Percussive Organ",
    19: "Rock Organ",
    20: "Church Organ",
    21: "Reed Organ",
    22: "Accordion",
    23: "Harmonica",
    24: "Tango Accordion",
    # Guitar
    25: "Acoustic Guitar (nylon)",
    26: "Acoustic Guitar (steel)",
    27: "Electric Guitar (jazz)",
    28: "Electric Guitar (clean)",
    29: "Electric Guitar (muted)",
    30: "Electric Guitar (overdriven)",
    31: "Electric Guitar (distortion)",
    32: "Electric Guitar (harmonics)",
    # Bass
    33: "Acoustic Bass",
    34: "Electric Bass (finger)",
    35: "Electric Bass (picked)",
    36: "Fretless Bass",
    37: "Slap Bass 1",
    38: "Slap Bass 2",
    39: "Synth Bass 1",
    40: "Synth Bass 2",
    # Strings
    41: "Violin",
    42: "Viola",
    43: "Cello",
    44: "Contrabass",
    45: "Tremolo Strings",
    46: "Pizzicato Strings",
    47: "Orchestral Harp",
    48: "Timpani",
    # Ensemble
    49: "String Ensemble 1",
    50: "String Ensemble 2",
    51: "Synth Strings 1",
    52: "Synth Strings 2",
    53: "Choir Aahs",
    54: "Voice Oohs (or Doos)",
    55: "Synth Voice or Solo Vox",
    56: "Orchestra Hit",
    # Brass
    57: "Trumpet",
    58: "Trombone",
    59: "Tuba",
    60: "Muted Trumpet",
    61: "French Horn",
    62: "Brass Section",
    63: "Synth Brass 1",
    64: "Synth Brass 2",
    # Reed
    65: "Soprano Sax",
    66: "Alto Sax",
    67: "Tenor Sax",
    68: "Baritone Sax",
    69: "Oboe",
    70: "English Horn",
    71: "Bassoon",
    72: "Clarinet",
    # Pipe
    73: "Piccolo",
    74: "Flute",
    75: "Recorder",
    76: "Pan Flute",
    77: "Blown bottle",
    78: "Shakuhachi",
    79: "Whistle",
    80: "Ocarina",
    # Synth Lead
    81: "Lead 1 (square)",
    82: "Lead 2 (sawtooth)",
    83: "Lead 3 (calliope)",
    84: "Lead 4 (chiff)",
    85: "Lead 5 (charang, a guitar-like lead)",
    86: "Lead 6 (space voice)",
    87: "Lead 7 (fifths)",
    88: "Lead 8 (bass and lead)",
    # Synth Pad
    89: "Pad 1 (new age or fantasia, a warm pad stacked with a bell)",
    90: "Pad 2 (warm)",
    91: "Pad 3 (polysynth or poly)",
    92: "Pad 4 (choir)",
    93: "Pad 5 (bowed glass or bowed)",
    94: "Pad 6 (metallic)",
    95: "Pad 7 (halo)",
    96: "Pad 8 (sweep)",
    # Synth Effects
    97: "FX 1 (rain)",
    98: "FX 2 (soundtrack, a bright perfect fifth pad)",
    99: "FX 3 (crystal)",
    100: "FX 4 (atmosphere, usually a nylon-like sound)",
    101: "FX 5 (brightness)",
    102: "FX 6 (goblins)",
    103: "FX 7 (echoes or echo drops)",
    104: "FX 8 (sci-fi or star theme)",
    # Ethnic
    105: "Sitar",
    106: "Banjo",
    107: "Shamisen",
    108: "Koto",
    109: "Kalimba",
    110: "Bag pipe",
    111: "Fiddle",
    112: "Shanai",
    # Percussive
    113: "Tinkle Bell",
    114: "Agogô",
    115: "Steel Drums",
    116: "Woodblock",
    117: "Taiko Drum",
    118: "Melodic Tom or 808 Toms",
    119: "Synth Drum",
    120: "Reverse Cymbal",
    # Sound Effects
    121: "Guitar Fret Noise",
    122: "Breath Noise",
    123: "Seashore",
    124: "Bird Tweet",
    125: "Telephone Ring",
    126: "Helicopter",
    127: "Applause",
    128: "Gunshot",
}
