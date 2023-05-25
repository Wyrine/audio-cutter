# MP3 Cutter

This Python script cuts a portion of an MP3 file from a starting timestamp to an ending timestamp. The input MP3 file, the output file, the start time, and the end time are provided as command-line arguments. This script uses the `pydub` library and assumes that `ffmpeg` is installed and available in the system's PATH.

## Dependencies

- Python 3
- pydub
- ffmpeg

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
./cut_mp3.py -i input.mp3 -o output.mp3 -s 1m30s -e 2m15s
```

This will cut the MP3 file from 1 minute 30 seconds to 2 minutes 15 seconds and save the result to `output.mp3`.

The script supports arbitrary timestamps for the start and end times. These can be in the following formats:

* `XmYs` - X minutes and Y seconds
* `XhYmZs` - X hours, Y minutes, and Z seconds
* `Xs` - X seconds

The start and end times are inclusive. That is, the resulting audio clip will start at the start time and end at the end time.

The script expects the arguments in the following format:

* `-i` or `--input_file`: The mp3 file to cut.
* `-o` or `--output_file`: The file to save the cut mp3 to.
* `-s` or `--start_time`: The start time in XmYs or XhYmZs format.
* `-e` or `--end_time`: The end time in XmYs or XhYmZs format.

All these arguments are required. You can use either the short version (`-i`, `-o`, `-s`, `-e`) or the long version (`--input_file`, `--output_file`, `--start_time`, `--end_time`).