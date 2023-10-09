#!/usr/bin/env python3

"""
A script to cut a portion of an audio file from a starting timestamp to an ending timestamp.
It can also download a YouTube video, convert it to audio, and cut a portion of the audio.

Usage: 
  python cut_audio.py -i input.mp3 -o output.mp3 -s 1m30s -e 2m15s
  python cut_audio.py -u "youtube-url" -o output.mp3 -s 1m30s -e 2m15s

The script takes 5 command line arguments:
1. input-file - The local audio file to cut.
2. youtube-url - The YouTube URL to download, convert to audio, and cut.
3. output-file - The file to save the cut audio to.
4. start-time - The start time in an arbitrary format (e.g., XmYs or XhYmZs). Default is the beginning of the audio.
5. end-time - The end time in the same format as start_time. Default is the end of the audio.

Only one of input_file and youtube_url should be provided.

This script uses the pydub and youtube_dl libraries and assumes that ffmpeg is installed and available in the system's PATH.
"""

import argparse
import os
import re
import youtube_dl
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


def download_audio(youtube_url: str, output_file: str, speed: float) -> None:
    """Download a YouTube video, convert it to audio, and save it to a file."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'postprocessors': [
            {
                'key': "ExecAfterDownload",
                'exec_cmd': f"ffmpeg -i {{}} -vn -af \"atempo={speed}\" processed_{{}}; rm {{}}; mv processed_{{}} {{}}",
            },
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Cut audio files or YouTube videos.')
    parser = argparse.ArgumentParser(
        description='Cut audio files or YouTube videos.')
    parser.add_argument('-i', '--input-file', type=str,
                        required=False, help='Input audio file')
    parser.add_argument('-u', '--youtube-url', type=str,
                        required=False, help='YouTube URL')
    parser.add_argument('-o', '--output-file', type=str,
                        required=True, help='Output audio file')
    parser.add_argument('-s', '--start-time', type=parse_time, required=False,
                        default=None, help='Start time in XmYs or XhYmZs format')
    parser.add_argument('-e', '--end-time', type=parse_time, required=False,
                        default=None, help='End time in XmYs or XhYmZs format')
    parser.add_argument('-sp', '--speed', type=float, required=False,
                        default=1.0, help='Speed to play audio at')
    args = parser.parse_args()

    if args.youtube_url and args.input_file:
        raise ValueError(
            'Only one of input_file and youtube_url should be provided.')

    if args.youtube_url:
        download_audio(args.youtube_url, args.output_file, args.speed)
        input_file = args.output_file
    else:
        input_file = args.input_file

    cut_audio(input_file, args.output_file, args.start_time, args.end_time)


if __name__ == "__main__":
    main()
