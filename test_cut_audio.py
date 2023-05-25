import pytest
from cut_audio import cut_audio, parse_time
from pydub import AudioSegment

def test_parse_time():
    # Test minutes and seconds
    assert parse_time("1m30s") == 90000

    # Test only seconds
    assert parse_time("45s") == 45000

    # Test hours, minutes, and seconds
    assert parse_time("1h15m30s") == 4530000

    # Test only hours
    assert parse_time("2h") == 7200000

    # Test none
    assert parse_time(None) == None

def test_cut_audio(tmp_path):
    # Generate a short silent audio segment for testing
    silence = AudioSegment.silent(duration=10000)  # duration in milliseconds
    test_audio_file = tmp_path / "test_audio.mp3"
    silence.export(str(test_audio_file), format="mp3")

    # Test the cut_audio function
    output_file = tmp_path / "output.mp3"
    cut_audio(str(test_audio_file), str(output_file), parse_time("2s"), parse_time("4s"))

    # Load the output file and check its duration
    output_audio = AudioSegment.from_file(str(output_file))
    assert len(output_audio) == 2000  # duration should be 2 seconds

