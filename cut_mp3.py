#!/usr/bin/env python3

"""
A script to cut a portion of an mp3 file from a starting timestamp to an ending timestamp.

Usage: python cut_mp3.py -i input.mp3 -o output.mp3 -s 1m30s -e 2m15s

The script takes 4 command line arguments:
1. input_file - The mp3 file to cut.
2. output_file - The file to save the cut mp3 to.
3. start_time - The start time in an arbitrary format (e.g., XmYs or XhYmZs).
4. end_time - The end time in the same format as start_time.

The start and end times are inclusive.

This script uses the pydub library and assumes that ffmpeg is installed and available in the system's PATH.
"""

import argparse
import re
from pydub import AudioSegment

def parse_time(time_str: str) -> int:
    """Parses a time string in an arbitrary format (XmYs, XhYmZs, etc.) and returns the time in milliseconds."""
    time_str = time_str.lower()
    hours = minutes = seconds = 0
    match = re.search(r'(\d+)h', time_str)
    if match:
        hours = int(match.group(1))
    match = re.search(r'(\d+)m', time_str)
    if match:
        minutes = int(match.group(1))
    match = re.search(r'(\d+)s', time_str)
    if match:
        seconds = int(match.group(1))
    return ((hours * 60 + minutes) * 60 + seconds) * 1000

def cut_mp3(input_file: str, output_file: str, start_time: int, end_time: int) -> None:
    """Cuts an mp3 file from start_time to end_time."""
    audio = AudioSegment.from_mp3(input_file)
    cut_audio = audio[start_time:end_time]
    cut_audio.export(output_file, format="mp3")

def main() -> None:
    parser = argparse.ArgumentParser(description='Cut mp3 files.')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input mp3 file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output mp3 file')
    parser.add_argument('-s', '--start_time', type=parse_time, required=True, help='Start time in XmYs or XhYmZs format')
    parser.add_argument('-e', '--end_time', type=parse_time, required=True, help='End time in XmYs or XhYmZs format')
    args = parser.parse_args()

    cut_mp3(args.input_file, args.output_file, args.start_time, args.end_time)

if __name__ == "__main__":
    main()
