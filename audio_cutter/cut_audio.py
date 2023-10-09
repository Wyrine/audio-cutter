#!/usr/bin/env python3

"""
A script to cut a portion of an audio file from a starting timestamp to an ending timestamp.
It can also download a media file from a YouTube or SoundCloud URL, optionally speed up the audio,
convert it to an audio file, and cut a portion of the audio.

Usage: 
  python cut_audio.py -i input.mp3 -o output.mp3 -s 1m30s -e 2m15s
  python cut_audio.py -u "media-url" -o output.mp3 -s 1m30s -e 2m15s -sp 1.5

The script takes six command line arguments:
1. input-file (-i, --input-file): The local audio file to cut.
2. media-url (-u, --url): The YouTube or SoundCloud URL to download, optionally speed up, convert to audio, and cut.
3. output-file (-o, --output-file): The file to save the cut audio to. Default is 'result.mp3'.
4. start-time (-s, --start-time): The start time in an arbitrary format (e.g., XmYs or XhYmZs). Default is the beginning of the audio.
5. end-time (-e, --end-time): The end time in the same format as start_time. Default is the end of the audio.
6. speed (-sp, --speed): The speed to play the audio at, e.g., 1.5 for 1.5x speed. Default is 1.0 (normal speed).

Only one of input_file and media_url should be provided.

This script uses the pydub, youtube_dl, and ffmpeg libraries and assumes that ffmpeg is installed and available in the system's PATH.
"""

import argparse
import os
import re
import youtube_dl
from pydub import AudioSegment
from typing import Optional


def _parse_time(time_str: Optional[str]) -> Optional[int]:
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


def _cut_audio(input_file: str, output_file: str, start_time: Optional[int], end_time: Optional[int]) -> None:
    """Cuts an audio file from start_time to end_time."""
    audio = AudioSegment.from_file(input_file)
    audio_snippet = audio[start_time:end_time]
    audio_snippet.export(output_file, format=output_file.split('.')[-1])


def _download_audio(url: str, output_file: str, speed: float) -> None:
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
        ydl.download([url])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Cut audio files or media from URLs.')
    parser.add_argument('-i', '--input-file', type=str,
                        required=False, help='Input audio file')
    parser.add_argument('-u', '--url', type=str,
                        required=False, help='Media URL')
    parser.add_argument('-o', '--output-file', help='Output audio file',
                        default='result.mp3', type=str, required=False)
    parser.add_argument('-s', '--start-time', type=_parse_time, required=False,
                        default=None, help='Start time in XmYs or XhYmZs format')
    parser.add_argument('-e', '--end-time', type=_parse_time, required=False,
                        default=None, help='End time in XmYs or XhYmZs format')
    parser.add_argument('-sp', '--speed', type=float, required=False,
                        default=1.0, help='Speed to play audio at')
    return parser.parse_args()


def process(url: str = None, input_file: str = None, output_file: str = "result.mp3", start_time: str | int = None, end_time: str | int = None, speed: float = 1.0):
    if not (url or input_file):
        raise ValueError(
            'One of input_file and url should be provided.')
    elif url and input_file:
        raise ValueError(
            'Only one of input_file and url should be provided.')

    if isinstance(start_time, str):
        start_time = _parse_time(start_time)
    if isinstance(end_time, str):
        end_time = _parse_time(end_time)

    if url:
        _download_audio(url, output_file, speed)
        input_file = output_file
    else:
        input_file = input_file

    _cut_audio(input_file, output_file, start_time, end_time)


if __name__ == "__main__":
    args = _parse_args()
    process(url=args.url, input_file=args.input_file, output_file=args.output_file,
            start_time=args.start_time, end_time=args.end_time, speed=args.speed)
