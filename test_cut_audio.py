import pytest
from cut_audio import _cut_audio, _parse_time
from pydub import AudioSegment


def test_parse_time():
    # Test minutes and seconds
    assert _parse_time("1m30s") == 90000

    # Test only seconds
    assert _parse_time("45s") == 45000

    # Test hours, minutes, and seconds
    assert _parse_time("1h15m30s") == 4530000

    # Test only hours
    assert _parse_time("2h") == 7200000

    # Test none
    assert _parse_time(None) == None


def test_cut_audio(tmp_path):
    # Generate a short silent audio segment for testing
    silence = AudioSegment.silent(duration=10000)  # duration in milliseconds
    test_audio_file = str(tmp_path / "test_audio.mp3")
    silence.export(test_audio_file, format="mp3")

    # Test the cut_audio function
    output_file = str(tmp_path / "output.mp3")
    _cut_audio(test_audio_file, output_file,
               _parse_time("2s"), _parse_time("4s"))

    # Load the output file and check its duration
    output_audio = AudioSegment.from_file(output_file)
    assert len(output_audio) == 2000  # duration should be 2 seconds
