#!/usr/bin/env python3

"""
A script to cut a portion of an audio file from a starting timestamp to an ending timestamp.

Usage: python cut_audio.py -i input.mp3 -o output.mp3 -s 1m30s -e 2m15s

The script takes 4 command line arguments:
1. input_file - The audio file to cut.
2. output_file - The file to save the cut audio to.
3. start_time - The start time in an arbitrary format (e.g., XmYs or XhYmZs). Default is the beginning of the audio.
4. end_time - The end time in the same format as start_time. Default is the end of the audio.

The start and end times are inclusive.

This script uses the pydub library and assumes that ffmpeg is installed and available in the system's PATH.
"""

import argparse
import re
from pydub import AudioSegment
from typing import Optional

def parse_time(time_str: Optional[str]) -> Optional[int]:
    """Parses a time string in an arbitrary format (XmYs, XhYmZs, etc.) and returns the time in milliseconds."""
    if time_str is None:
        return None

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

def cut_audio(input_file: str, output_file: str, start_time: Optional[int], end_time: Optional[int]) -> None:
    """Cuts an audio file from start_time to end_time."""
    audio = AudioSegment.from_file(input_file)
    cut_audio = audio[start_time:end_time]
    cut_audio.export(output_file, format=output_file.split('.')[-1])

def main() -> None:
    parser = argparse.ArgumentParser(description='Cut audio files.')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input audio file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output audio file')
    parser.add_argument('-s', '--start_time', type=parse_time, required=False, default=None, help='Start time in XmYs or XhYmZs format')
    parser.add_argument('-e', '--end_time', type=parse_time, required=False, default=None, help='End time in XmYs or XhYmZs format')
    args = parser.parse_args()

    cut_audio(args.input_file, args.output_file, args.start_time, args.end_time)

if __name__ == "__main__":
    main()
