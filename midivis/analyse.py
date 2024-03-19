import hashlib
import sqlite3
import sys
from collections import Counter
from datetime import timedelta
from pathlib import Path
from time import monotonic

from mido import MidiFile


def analyse_files(base_path: Path) -> None:
    notes = Counter()
    note_ranges = Counter()
    channels = Counter()
    programs = Counter()

    start = monotonic()

    paths = list(base_path.glob("**/*.mid", case_sensitive=False))
    paths += list(base_path.glob("**/*.midi", case_sensitive=False))
    paths.sort()

    print(f"Globbed {len(paths)} files in {timedelta(seconds=monotonic() - start)}")

    fails = 0
    n = 0

    conn = init_db()
    cursor = conn.cursor()

    try:
        for n, path in enumerate(paths):
            relative_path_str = str(path.relative_to(base_path))
            if cursor.execute(
                "select 1 from tracks where file_path = ?", (relative_path_str,)
            ).fetchall():
                print(f"Track already processed: {relative_path_str}")
                continue
            try:
                midi_file = MidiFile(str(path))
            except Exception:
                print(f"Error opening {n} of {len(paths)} - {relative_path_str}")
                fails += 1
                continue

            with open(path, "rb") as f:
                file_hash = hashlib.file_digest(f, "blake2b")

            this_channels = set()
            this_programs = set()
            note_count = 0
            max_note = -1
            min_note = 256

            for i, track in enumerate(midi_file.tracks):
                for message in track:
                    match message.type:
                        case "note_on":
                            note_count += 1
                            notes[message.note] += 1
                            this_channels.add(message.channel)
                            max_note = max(max_note, message.note)
                            min_note = min(min_note, message.note)
                        case "program_change":
                            this_programs.add(message.program)

            try:
                runtime_secs = midi_file.length
            except ValueError:
                runtime_secs = None

            row_params = {
                "file_path": relative_path_str,
                "file_name": path.stem,
                "file_size_bytes": path.stat().st_size,
                "file_hash_blake2b": file_hash.hexdigest(),
                "runtime_secs": runtime_secs,
                "channel_count": len(this_channels),
                "note_count": note_count,
                "program_count": len(this_programs),
                "note_max": max_note if note_count else None,
                "note_min": min_note if note_count else None,
            }

            cursor.execute(
                """
                INSERT INTO tracks (
                    file_path,
                    file_name,
                    file_size_bytes,
                    file_hash_blake2b,
                    runtime_secs,
                    channel_count,
                    note_count,
                    program_count,
                    note_max,
                    note_min
                ) VALUES (
                    :file_path,
                    :file_name,
                    :file_size_bytes,
                    :file_hash_blake2b,
                    :runtime_secs,
                    :channel_count,
                    :note_count,
                    :program_count,
                    :note_max,
                    :note_min
                )
            """,
                row_params,
            )
            conn.commit()

            note_ranges[max_note - min_note if note_count else 0] += 1
            channels.update(this_channels)
            programs.update(this_programs)
    except KeyboardInterrupt:
        pass

    print("\nChannels")
    draw_hist(channels)
    print("\nNotes")
    draw_hist(notes)
    print("\nPrograms")
    draw_hist(programs)
    print("\nNote Ranges")
    draw_hist(note_ranges)

    print(f"\n{fails} failed out of {n} processed")
    print(f"Total time: {timedelta(seconds=monotonic() - start)}")


def draw_hist(data: Counter) -> None:
    if not data:
        print("No data")
        return
    max_val = max(data.values())
    for i in range(max(data.keys()) + 1):
        bar = "\u25ac" * int(data[i] / max_val * 80)
        print(f"{i:3d} | {bar:80s} | {data[i]:6d}")


def init_db():
    con = sqlite3.connect("midi.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id INTEGER PRIMARY KEY,
            -- file info
            file_path TEXT NOT NULL UNIQUE,
            file_name TEXT NOT NULL,
            file_size_bytes INTEGER NOT NULL,
            file_hash_blake2b TEXT NOT NULL,
            -- track info
            runtime_secs REAL,  -- NULLable because Mido says asynchronous midi files have no defined runtime
            channel_count INTEGER NOT NULL,
            note_count INTEGER NOT NULL,
            program_count INTEGER NOT NULL,
            note_max INTEGER,
            note_min INTEGER
        )
    """)

    return con


def main():
    base_path = sys.argv[1] if len(sys.argv) >= 2 else "."
    analyse_files(Path(base_path))


if __name__ == "__main__":
    main()
