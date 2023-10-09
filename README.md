# Audio Cutter

![Tests](https://github.com/Wyrine/audio-cutter/actions/workflows/.github/workflows/test.yml/badge.svg?branch=main)

This Python script cuts a portion of an audio file from a starting timestamp to an ending timestamp. The input audio file, the output file, the start time, and the end time are provided as command-line arguments. If not provided, the start time defaults to the beginning of the audio file and the end time defaults to the end of the audio file. This script uses the `pydub` library and assumes that `ffmpeg` is installed and available in the system's PATH.

## Dependencies

- Python 3
- pydub
- ffmpeg
- youtube-dl

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure `ffmpeg` is installed and available in your system's PATH. If it's not, you can download it from the official [ffmpeg](https://www.ffmpeg.org/) site and install it. The installation process can vary based on the system you're using.

## Usage

Run the script from the command line like this:

```bash
./cut_audio.py -i input.mp3 -o output.mp3 -s 1m30s -e 2m15s
```

This will cut the MP3 file from 1 minute 30 seconds to 2 minutes 15 seconds and save the result to `output.mp3`.

The script supports arbitrary timestamps for the start and end times. These can be in the following formats:

- `XmYs` - X minutes and Y seconds
- `XhYmZs` - X hours, Y minutes, and Z seconds
- `Xs` - X seconds

The start and end times are optional and inclusive. That is, the resulting audio clip will start at the start time and end at the end time. If not provided, the start time defaults to the beginning of the audio file and the end time defaults to the end of the audio file.

The script expects the arguments in the following format:

- `-i` or `--input-file`: The audio file to cut.
- `-u` or `--youtube-url`: The url to use instead of the `--input-file` arg.
- `-o` or `--output-file`: The file to save the cut audio to.
- `-s` or `--start-time`: The start time in XmYs or XhYmZs format. Optional.
- `-e` or `--end-time`: The end time in XmYs or XhYmZs format. Optional.

You can use either the short version (`-i`, `-o`, `-s`, `-e`, `-u`) or the long version (`--input-file`, `--output-file`, `--start-time`, `--end-time`, `--youtube-url`) of the command-line arguments.
